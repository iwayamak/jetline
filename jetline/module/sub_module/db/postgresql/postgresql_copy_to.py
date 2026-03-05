"""PostgreSQL からファイルへ出力するサブモジュール."""

from .....command.db.postgresql.postgresql_copy_to_command import PostgreSQLCopyToCommand
from ....sub_module_parameter.db.postgresql.postgresql_copy_to_parameter import (
    PostgreSQLCopyToParameter,
)
from .abc.postgresql_sub_module import PostgreSQLSubModule


class PostgreSQLCopyTo(PostgreSQLSubModule):
    """SQL 結果を CSV などへエクスポートする."""

    def __init__(self, param: PostgreSQLCopyToParameter):
        """COPY TO サブモジュールを初期化する.

        Args:
            param: COPY TO 用パラメータ.
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する."""
        component = self.resolve_postgresql_component()
        command = PostgreSQLCopyToCommand(
            component,
            self._load_sql(),
            self._parameter.csv_file_name.get(),
            self._parameter.delimiter.get(),
            self._parameter.null_str.get(),
            self._parameter.header.get(),
            self._parameter.quote.get(),
            self._parameter.escape.get(),
            self._parameter.force_quote_list.get(),
            self._parameter.encoding.get(),
            self._parameter.gzip.get(),
        )
        command.execute()
        self._result_local_file_list = [self._parameter.csv_file_name.get()]

    def _load_sql(self) -> str:
        """SQL ファイルを入力値で展開して読み込む."""
        return self.load_sql_from_parameter()

    def tear_down(self):
        """実行後処理を行う."""
        super().tear_down()
