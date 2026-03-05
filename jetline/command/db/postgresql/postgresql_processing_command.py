"""PostgreSQL 汎用 SQL 実行コマンド."""

from ....container.component.postgresql_component import PostgreSQLComponent
from .abc.postgresql_command import PostgreSQLCommand


class PostgreSQLProcessingCommand(PostgreSQLCommand):
    """任意 SQL を実行する."""

    def __init__(self, component: PostgreSQLComponent, sql_str: str):
        """SQL 実行コマンドを初期化する.

        Args:
            component: PostgreSQL コンポーネント.
            sql_str: 実行対象 SQL.
        """
        super().__init__(component, sql_str)

    def run(self):
        """SQL を実行してコミットする."""
        super().run()
        self.execute_query(commit=True)
