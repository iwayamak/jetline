"""Container のユニットテスト。."""

from jetline.container.container import Container
from test.abc.base_test_case import BaseTestCase


class TestContainer(BaseTestCase):
    """Container のコンポーネント解決を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_container(self):
        """コンポーネントキーから PostgreSQLComponent を取得できることを確認する。."""
        component = Container().component("POSTGRESQL_COMPONENT.ID=TEST_COMPONENT")
        self.assertEqual(component.database, "test_database")
