
"""YAML で定義された SubModule 群を実行するモジュール本体。."""

import logging
import os

from retry import retry

from ..config.config import Config
from ..container.container import Container
from ..exception.exec_yaml_error import ExecYamlError
from ..module.sub_module.result.sub_module_result import SubModuleResult
from ..module.sub_module.sub_module_creator import SubModuleCreator
from ..parser.kicker_args_parser import KickerArgsParser, RetryOptions
from ..share_parameter.share_parameter import ShareParameter
from ..util.yaml_util import YamlUtil

logger = logging.getLogger('jetline')


class Module:
    """ジョブ実行のライフサイクルを管理する。."""

    KEY_SUB_MODULE = 'sub_module'
    KEY_SUB_MODULE_NAME = 'name'
    KEY_SUB_MODULE_PARAM = 'param'
    KEY_SUB_MODULE_MODE = 'mode'

    _retry_options = RetryOptions(tries=1, delay=1, backoff=1, jitter=0, max_delay=None)
    _component_resolver = Container.component

    def __init__(self, exec_yaml_path: str, exec_date: str):
        """実行対象 YAML を読み込み、モジュール状態を初期化する。.

        Args:
            exec_yaml_path: 実行YAMLファイルのパス。
            exec_date: 実行日（YYYYMMDD）。
        """
        ShareParameter.exec_yaml_path = exec_yaml_path
        ShareParameter.exec_date = exec_date
        ShareParameter.exec_yaml = YamlUtil.load_file(exec_yaml_path)
        self._sub_module_obj_list = []
        self._retry_options = self.__class__._retry_options
        self._component_resolver = self.__class__._component_resolver

    def _validate_exec_yaml(self):
        """実行YAMLの最低限の構造を検証する。."""
        exec_yaml = ShareParameter.exec_yaml
        if not isinstance(exec_yaml, dict):
            raise ExecYamlError('exec yaml must be a dict')
        if self.KEY_SUB_MODULE not in exec_yaml:
            raise ExecYamlError(f'missing key: {self.KEY_SUB_MODULE}')
        if not isinstance(exec_yaml[self.KEY_SUB_MODULE], list):
            raise ExecYamlError(f'{self.KEY_SUB_MODULE} must be a list')

    @classmethod
    def _normalize_sub_module_spec(cls, sub_module_spec: dict):
        """サブモジュール定義を検証し、必要値を返す。.

        Args:
            sub_module_spec: YAML上のサブモジュール定義。

        Returns:
            tuple[str, dict, str]: サブモジュール名、パラメータ、モード。
        """
        required_keys = (cls.KEY_SUB_MODULE_NAME, cls.KEY_SUB_MODULE_PARAM, cls.KEY_SUB_MODULE_MODE)
        missing = [key for key in required_keys if key not in sub_module_spec]
        if missing:
            raise ExecYamlError(f'missing sub_module keys: {", ".join(missing)}')
        if not isinstance(sub_module_spec[cls.KEY_SUB_MODULE_PARAM], dict):
            raise ExecYamlError(f'{cls.KEY_SUB_MODULE_PARAM} must be a dict')
        return (
            sub_module_spec[cls.KEY_SUB_MODULE_NAME],
            sub_module_spec[cls.KEY_SUB_MODULE_PARAM],
            sub_module_spec[cls.KEY_SUB_MODULE_MODE],
        )

    def _build_sub_modules(self):
        """実行対象サブモジュール一覧を構築する。.

        Returns:
            list: サブモジュールオブジェクトの配列。
        """
        sub_module_specs = ShareParameter.exec_yaml[self.KEY_SUB_MODULE]
        sub_modules = []
        for sub_module_spec in sub_module_specs:
            if not isinstance(sub_module_spec, dict):
                raise ExecYamlError('each sub_module item must be a dict')

            (
                sub_module_name,
                sub_module_param,
                sub_module_mode,
            ) = self._normalize_sub_module_spec(sub_module_spec)
            if sub_module_name not in Config.AVAILABLE_SUB_MODULE:
                raise ExecYamlError(f'this sub_module using is forbidden : {sub_module_name}')

            created = SubModuleCreator.create_sub_module_list(
                sub_module_name,
                sub_module_param,
                sub_module_mode,
                component_resolver=self._component_resolver,
            )
            if len(created) == 0:
                raise ExecYamlError(f'sub_module failed: {sub_module_name}')
            sub_modules.extend(created)
        return sub_modules

    def set_up(self):
        """実行前準備を行う。."""
        ShareParameter.sub_module_result = SubModuleResult()
        ShareParameter.command_metrics = {
            "total": 0,
            "succeeded": 0,
            "failed": 0,
            "by_name": {},
            "by_sub_module": {},
            "failures": [],
        }
        SubModuleCreator.reset_metrics()
        self._validate_exec_yaml()
        self._sub_module_obj_list = self._build_sub_modules()
        logger.info("SubModuleCreator metrics: %s", SubModuleCreator.metrics())

    def _execute_sub_modules_once(self):
        """サブモジュールを1試行分実行する。."""
        ShareParameter.tries_count += 1
        if ShareParameter.tries_count > 1:
            logger.info(f'Try count is {ShareParameter.tries_count}')

        for seq, sub_module_obj in enumerate(self._sub_module_obj_list):
            logger.info(f'seq {seq + 1}: {type(sub_module_obj).__name__}')
            sub_module_obj.execute()

    def execute(self):
        """リトライ設定を適用してサブモジュールを実行する。."""
        ShareParameter.tries_count = 0
        retryable_execute = retry(
            tries=self._retry_options.tries,
            delay=self._retry_options.delay,
            backoff=self._retry_options.backoff,
            jitter=self._retry_options.jitter,
            max_delay=self._retry_options.max_delay,
            logger=logging,
        )(self._execute_sub_modules_once)
        retryable_execute()

    def tear_down(self):
        """実行後処理を行う。.

        実行結果を `*_result.yaml` へ出力する。
        """
        result = ShareParameter.sub_module_result
        if result is None:
            return

        command_metrics = dict(ShareParameter.command_metrics or {})
        result.set_creator_metrics(SubModuleCreator.metrics())
        result.set_command_metrics(command_metrics)
        result.set_sub_module_summary(
            SubModuleResult.build_sub_module_summary(command_metrics)
        )
        result.set_execution_context(self._build_execution_context_metadata())
        result_file_path = self._resolve_result_file_path()
        YamlUtil.write_file(result_file_path, result.as_dict())
        logger.info("result yaml: %s", result_file_path)

    def _resolve_result_file_path(self) -> str:
        """結果 YAML の出力先パスを返す。"""
        batch_name = ShareParameter.batch_name
        if not batch_name:
            exec_yaml_path = ShareParameter.exec_yaml_path or "jetline"
            batch_name = os.path.splitext(os.path.basename(exec_yaml_path))[0]
        return f"{batch_name}{SubModuleResult.FILE_NAME_SUFFIX}"

    def _build_execution_context_metadata(self) -> dict:
        """結果YAMLへ出力する実行コンテキストを構築する。"""
        retry_options = {
            "tries": self._retry_options.tries,
            "delay": self._retry_options.delay,
            "backoff": self._retry_options.backoff,
            "jitter": self._serialize_jitter(self._retry_options.jitter),
            "max_delay": self._retry_options.max_delay,
        }
        return {
            "exec_yaml_path": ShareParameter.exec_yaml_path,
            "exec_date": ShareParameter.exec_date,
            "dry_run_mode": ShareParameter.dry_run_mode,
            "tries_count": ShareParameter.tries_count,
            "retry_options": retry_options,
            "command_metrics": dict(ShareParameter.command_metrics or {}),
        }

    @staticmethod
    def _serialize_jitter(jitter):
        """YAML 互換のため jitter をシリアライズ可能な型へ変換する。"""
        if isinstance(jitter, tuple):
            return list(jitter)
        return jitter

    @classmethod
    def configure_retry_options(cls, retry_options: RetryOptions):
        """リトライ設定を更新する。.

        Args:
            retry_options: 反映するリトライ設定。
        """
        cls._retry_options = retry_options

    @classmethod
    def configure_component_resolver(cls, component_resolver):
        """コンポーネント解決関数を注入する。.

        Args:
            component_resolver: `component_key` を受け取りコンポーネントを返す関数。
        """
        cls._component_resolver = component_resolver

    @classmethod
    def parse_kick_args(cls, argv):
        """CLI引数を解析し、実行設定へ反映する。.

        Args:
            argv: 引数配列。

        Returns:
            tuple[str, str, Optional[str]]: YAMLパス、実行日、作業ディレクトリ。
        """
        options = KickerArgsParser(argv).options()
        ShareParameter.dry_run_mode = options.dry_run
        cls.configure_retry_options(options.retry)
        return options.yaml_file, options.exec_date, options.working_dir
