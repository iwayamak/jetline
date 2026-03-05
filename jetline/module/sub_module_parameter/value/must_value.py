"""必須値ラッパー。."""

from ....exception.sub_module_parameter_error import SubModuleParameterError
from .abc.value import Value


class MustValue(Value):
    """`None` を許容しない値ラッパー。."""

    def __init__(self, value, display=None):
        """必須値を初期化する。."""
        if value is None:
            raise SubModuleParameterError("MustValue", "None")
        super().__init__(value, display)
