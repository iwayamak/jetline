"""SubModuleParameterError のユニットテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestSubModuleParameterError(BaseTestCase):
    """SubModuleParameterError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """SubModuleParameterError が送出できることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            raise SubModuleParameterError("validator_name", "target")
