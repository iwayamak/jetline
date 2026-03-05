"""PostgreSQL の汎用 SQL 実行サブモジュール."""

from .....command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from ....sub_module_parameter.db.postgresql.postgresql_processing_parameter import (
    PostgreSQLProcessingParameter,
)
from .abc.postgresql_sub_module import PostgreSQLSubModule


class PostgreSQLProcessing(PostgreSQLSubModule):
    """SQL ファイルを読み込み、PostgreSQL へ実行する."""

    def __init__(self, param: PostgreSQLProcessingParameter):
        """SQL 実行サブモジュールを初期化する.

        Args:
            param: SQL 実行パラメータ.
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する."""
        component = self.resolve_postgresql_component()
        command = PostgreSQLProcessingCommand(component, self._load_sql())
        command.execute()

    def _load_sql(self) -> str:
        """SQL ファイルを入力値で展開して読み込む."""
        return self.load_sql_from_parameter()

    def tear_down(self):
        """実行後処理を行う."""
        super().tear_down()
