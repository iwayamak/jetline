
"""SubModule の共通実行基盤。"""

import datetime
import glob
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from ....container.container import Container
from ....share_parameter.share_parameter import ShareParameter
from ...sub_module.result.sub_module_result import SubModuleResult


@dataclass
class SubModuleExecutionState:
    """SubModule 実行時の状態を保持する。"""

    started_at: datetime.datetime | None = None
    ended_at: datetime.datetime | None = None
    processing_time_seconds: float | None = None
    succeeded: bool = False
    error: Exception | None = None


class SubModule(metaclass=ABCMeta):
    """各サブモジュールの実行テンプレート。"""

    def __init__(self, parameter, component_resolver: Callable[[str], object] | None = None):
        """サブモジュールを初期化する。

        Args:
            parameter: サブモジュールのパラメータオブジェクト。
            component_resolver: コンポーネント解決関数。
        """
        self._parameter = parameter
        self._processing_time = None
        self._result_local_file_list = None
        self._result_s3_file_list = None
        self._is_status = SubModuleResult.STATUS_ERROR
        self._start_datetime = None
        self._end_datetime = None
        self._state = SubModuleExecutionState()
        # 依存注入されない場合は既存実装と同様に Container を使う。
        self._component_resolver = component_resolver or Container.component

    @property
    def state(self) -> SubModuleExecutionState:
        """直近実行の状態を返す。"""
        return self._state

    def set_component_resolver(self, component_resolver: Callable[[str], object]):
        """コンポーネント解決関数を差し替える。

        Args:
            component_resolver: `component_key` を受け取りコンポーネントを返す関数。
        """
        self._component_resolver = component_resolver

    def resolve_component(self, key: str):
        """キーからコンポーネントを解決する。

        Args:
            key: コンポーネントキー。

        Returns:
            object: 解決したコンポーネント。
        """
        return self._component_resolver(key)

    def set_up(self):
        """実行前処理を行う。"""
        return None

    @abstractmethod
    def run(self):
        """サブモジュール本体を実行する。"""
        raise NotImplementedError

    def tear_down(self):
        """実行結果を共有結果へ追記する。"""
        ShareParameter.sub_module_result.append_result(
            self.__class__.__name__,
            self._start_datetime,
            self._end_datetime,
            self._processing_time,
            self._result_local_file_list,
            self._result_s3_file_list,
            self._is_status
        )

    def execute(self):
        """サブモジュールを1回実行する。"""
        self._state = SubModuleExecutionState()
        self._start_datetime = datetime.datetime.now()
        self._state.started_at = self._start_datetime
        previous_sub_module_name = ShareParameter.current_sub_module_name
        ShareParameter.current_sub_module_name = self.__class__.__name__
        try:
            self.set_up()
            self.run()
        except Exception as exc:
            self._state.error = exc
            raise
        else:
            self._is_status = SubModuleResult.STATUS_SUCCESS
            self._state.succeeded = True
        finally:
            try:
                self._end_datetime = datetime.datetime.now()
                self._state.ended_at = self._end_datetime
                self._processing_time = (
                    self._end_datetime - self._start_datetime
                ).total_seconds()
                self._state.processing_time_seconds = self._processing_time
                self.tear_down()
            finally:
                ShareParameter.current_sub_module_name = previous_sub_module_name

    @staticmethod
    def normalize_non_empty_paths(paths: Iterable[str] | None) -> list[str]:
        """空文字を除外したパス一覧へ正規化する。

        Args:
            paths: 正規化対象のパス列。`None` の場合は空配列を返す。

        Returns:
            list[str]: 空要素を取り除いたパス一覧。
        """
        if paths is None:
            return []
        return [path for path in paths if path]

    @staticmethod
    def expand_glob_patterns(
        patterns: Iterable[str],
        recursive: bool = False,
    ) -> list[str]:
        """パターン列をファイルパスへ展開する。

        Args:
            patterns: `glob` パターン列。
            recursive: `**` を再帰展開する場合は `True`。

        Returns:
            list[str]: 展開後のファイルパス一覧。処理順を安定化するためソート済み。
        """
        expanded_paths: list[str] = []
        for pattern in patterns:
            if not pattern:
                continue
            if glob.has_magic(pattern):
                expanded_paths.extend(glob.glob(pattern, recursive=recursive))
            else:
                expanded_paths.append(pattern)
        return sorted(expanded_paths)

    @staticmethod
    def get_last_result_local_paths() -> list[str]:
        """直前サブモジュールのローカル出力一覧を返す。

        Returns:
            list[str]: 直前サブモジュールで生成されたローカルファイル一覧。
        """
        result = ShareParameter.sub_module_result
        if result is None:
            return []
        last_paths = result.get_last_log_local_data_file_list()
        if last_paths is None:
            return []
        return list(last_paths)
