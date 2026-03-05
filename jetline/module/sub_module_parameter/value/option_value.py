"""任意値ラッパー。."""

from .abc.value import Value


class OptionValue(Value):
    """`None` の場合にデフォルト値を適用するラッパー。."""

    def __init__(self, value, default=None, display=None):
        """任意値を初期化する。."""
        resolved_value = default if value is None else value
        super().__init__(resolved_value, display)
