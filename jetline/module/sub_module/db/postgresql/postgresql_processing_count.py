"""PostgreSQL の件数検証付き実行サブモジュール."""

from .....command.db.postgresql.postgresql_processing_count_command import (
    PostgreSQLProcessingCountCommand,
)
from ....sub_module_parameter.db.postgresql.postgresql_processing_count_parameter import (
    PostgreSQLProcessingCountParameter,
)
from .abc.postgresql_sub_module import PostgreSQLSubModule


class PostgreSQLProcessingCount(PostgreSQLSubModule):
    """SQL 実行結果の件数に対してアサーションを行う."""

    def __init__(self, param: PostgreSQLProcessingCountParameter):
        """件数検証付き SQL 実行サブモジュールを初期化する.

        Args:
            param: 件数検証パラメータ.
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する."""
        component = self.resolve_postgresql_component()
        command = PostgreSQLProcessingCountCommand(
            component=component,
            sql_str=self._load_sql(),
            assert_eq=self._parameter.assert_eq.get(),
            assert_ne=self._parameter.assert_ne.get(),
            assert_ge=self._parameter.assert_ge.get(),
            assert_le=self._parameter.assert_le.get(),
        )
        command.execute()

    def _load_sql(self) -> str:
        """SQL ファイルを入力値で展開して読み込む."""
        return self.load_sql_from_parameter()

    def tear_down(self):
        """実行後処理を行う."""
        super().tear_down()
