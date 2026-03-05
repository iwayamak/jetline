"""ScpComponent のユニットテスト。."""

from jetline.container.container import Container
from test.abc.base_test_case import BaseTestCase


class TestScpComponent(BaseTestCase):
    """ScpComponent のプロパティ解決を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._component = Container.component("SCP_COMPONENT.ID=TEST_COMPONENT")
        super().__init__(*args, **kwargs)

    def test_user(self):
        """User が期待値であることを確認する。."""
        self.assertEqual(self._component.user, "test_user")

    def test_password(self):
        """Password が期待値であることを確認する。."""
        self.assertEqual(self._component.password, "test_password")

    def test_host(self):
        """Host が期待値であることを確認する。."""
        self.assertEqual(self._component.host, "test_host")

    def test_port(self):
        """Port が期待値であることを確認する。."""
        self.assertEqual(self._component.port, 22)
