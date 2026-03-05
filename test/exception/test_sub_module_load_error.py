"""SubModuleLoadError のユニットテスト。."""

from jetline.exception.sub_module_load_error import SubModuleLoadError
from test.abc.base_test_case import BaseTestCase


class TestSubModuleLoadError(BaseTestCase):
    """SubModuleLoadError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """SubModuleLoadError が送出できることを確認する。."""
        with self.assertRaises(SubModuleLoadError):
            raise SubModuleLoadError("test_sub_module")
