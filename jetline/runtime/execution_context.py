
"""実行コンテキストを ContextVar で管理する。."""

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field


@dataclass
class ExecutionContext:
    """1回の実行で共有される状態。."""

    exec_yaml_path: str | None = None
    exec_yaml: dict | None = None
    exec_date: str | None = None
    dry_run_mode: bool = False
    batch_name: str | None = None
    log_name: str | None = None
    log_dir: str | None = None
    sub_module_result: object | None = None
    working_dir: str | None = None
    success_return_code: int = 0
    error_return_code: int = 1
    tries_count: int = 0
    current_sub_module_name: str | None = None
    command_metrics: dict[str, object] = field(
        default_factory=lambda: {
            "total": 0,
            "succeeded": 0,
            "failed": 0,
            "by_name": {},
            "by_sub_module": {},
            "failures": [],
        }
    )


_CURRENT_CONTEXT: ContextVar[ExecutionContext | None] = ContextVar(
    'jetline_execution_context',
    default=None,
)


def new_execution_context() -> ExecutionContext:
    """新しい実行コンテキストを作成する。.

    Returns:
        ExecutionContext: 初期化済みコンテキスト。
    """
    return ExecutionContext()


def get_current_context() -> ExecutionContext:
    """現在の実行コンテキストを返す。.

    Returns:
        ExecutionContext: 現在のコンテキスト。未設定の場合は新規作成される。
    """
    context = _CURRENT_CONTEXT.get()
    if context is None:
        context = new_execution_context()
        _CURRENT_CONTEXT.set(context)
    return context


def set_current_context(context: ExecutionContext):
    """現在の実行コンテキストを設定する。.

    Args:
        context: 設定するコンテキスト。

    Returns:
        contextvars.Token: 復元用トークン。
    """
    return _CURRENT_CONTEXT.set(context)


def reset_current_context() -> ExecutionContext:
    """実行コンテキストを初期状態へ戻す。.

    Returns:
        ExecutionContext: 初期化後のコンテキスト。
    """
    context = new_execution_context()
    _CURRENT_CONTEXT.set(context)
    return context


@contextmanager
def use_execution_context(context: ExecutionContext) -> Iterator[ExecutionContext]:
    """指定したコンテキストを一時的に有効化する。.

    Args:
        context: 一時的に有効化するコンテキスト。

    Yields:
        ExecutionContext: 有効化中のコンテキスト。
    """
    token = set_current_context(context)
    try:
        yield context
    finally:
        _CURRENT_CONTEXT.reset(token)
