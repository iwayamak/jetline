"""ComponentLoadError のユニットテスト。."""

from jetline.exception.component_load_error import ComponentLoadError
from test.abc.base_test_case import BaseTestCase


class TestComponentLoadError(BaseTestCase):
    """ComponentLoadError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """ComponentLoadError が送出できることを確認する。."""
        with self.assertRaises(ComponentLoadError):
            raise ComponentLoadError("test_component")
