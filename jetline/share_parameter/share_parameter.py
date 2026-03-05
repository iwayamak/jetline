
"""旧 ShareParameter API の互換レイヤ。."""

from typing import Final

from ..runtime.execution_context import get_current_context, reset_current_context


class _ShareParameterMeta(type):
    """ExecutionContext の属性をクラス変数風に中継するメタクラス。."""

    _managed_keys: Final[set[str]] = {
        'exec_yaml_path',
        'exec_yaml',
        'exec_date',
        'dry_run_mode',
        'batch_name',
        'log_name',
        'log_dir',
        'sub_module_result',
        'working_dir',
        'success_return_code',
        'error_return_code',
        'tries_count',
        'current_sub_module_name',
        'command_metrics',
    }

    def __getattr__(cls, item):
        """管理対象キーへのアクセスを実行コンテキストへ委譲する。."""
        if item in cls._managed_keys:
            return getattr(get_current_context(), item)
        raise AttributeError(item)

    def __setattr__(cls, key, value):
        """管理対象キーへの代入を実行コンテキストへ委譲する。."""
        if key in cls._managed_keys:
            setattr(get_current_context(), key, value)
            return
        super().__setattr__(key, value)


class ShareParameter(metaclass=_ShareParameterMeta):
    """従来コード互換のためのプロキシ。."""

    @classmethod
    def reset(cls):
        """共有状態を初期化する。.

        Returns:
            ExecutionContext: 初期化後の実行コンテキスト。
        """
        return reset_current_context()
