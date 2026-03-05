"""PluginComponent のユニットテスト。."""

from jetline.container.container import Container
from test.abc.base_test_case import BaseTestCase


class TestPluginComponent(BaseTestCase):
    """PluginComponent のプロパティ解決を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._component = Container.component("PLUGIN_COMPONENT.ID=TEST_COMPONENT")
        super().__init__(*args, **kwargs)

    def test_param1(self):
        """param1 が期待値であることを確認する。."""
        self.assertEqual(self._component.param1, "Param_01")

    def test_param2(self):
        """param2 が期待値であることを確認する。."""
        self.assertEqual(self._component.param2, "Param_02")
