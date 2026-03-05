"""ファイルから PostgreSQL へ取り込むサブモジュール."""

from .....command.command_queue import CommandQueue
from .....command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from .....command.local.remove_command import RemoveCommand
from ....sub_module_parameter.db.postgresql.postgresql_copy_from_parameter import (
    PostgreSQLCopyFromParameter,
)
from .abc.postgresql_sub_module import PostgreSQLSubModule


class PostgreSQLCopyFrom(PostgreSQLSubModule):
    """CSV/TSV 等を PostgreSQL テーブルへ取り込む."""

    def __init__(self, param: PostgreSQLCopyFromParameter):
        """COPY FROM サブモジュールを初期化する.

        Args:
            param: COPY FROM 用パラメータ.
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する."""
        csv_file_name_list = self._resolve_input_files()
        component = self.resolve_postgresql_component()
        queue = CommandQueue()
        queue.add_command(
            PostgreSQLCopyFromCommand(
                component,
                self._parameter.table_name.get(),
                self._parameter.column_list.get(),
                csv_file_name_list,
                self._parameter.delimiter.get(),
                self._parameter.null_str.get(),
                self._parameter.header.get(),
                self._parameter.quote.get(),
                self._parameter.escape.get(),
                self._parameter.encoding.get(),
                self._parameter.gzip.get(),
            )
        )

        if self._parameter.remove_source_file.get():
            for csv_file_name in csv_file_name_list:
                queue.add_command(RemoveCommand(csv_file_name))
        queue.execute()

    def _resolve_input_files(self) -> list[str]:
        """COPY FROM の入力ファイル一覧を解決する.

        Returns:
            list[str]: 入力ファイルパス一覧.

        Raises:
            ValueError: 入力ソースが1件も解決できない場合.
        """
        csv_file_name_list = self._resolve_files_from_pattern()
        if self._parameter.use_last_result.get():
            # 直前サブモジュール結果を入力ファイルとして再利用する。
            csv_file_name_list = self.get_last_result_local_paths()
        normalized_files = self.normalize_non_empty_paths(csv_file_name_list)
        if not normalized_files:
            raise ValueError(
                "COPY FROM の入力ファイルがありません。"
                "csv_file_name または use_last_result を確認してください。"
            )
        return normalized_files

    def _resolve_files_from_pattern(self) -> list[str]:
        """`csv_file_name` パターンから入力ファイルを解決する.

        Returns:
            list[str]: 解決したファイル一覧。未設定時は空配列.
        """
        csv_glob = self._parameter.csv_file_name.get()
        if not csv_glob:
            return []
        return self.expand_glob_patterns([csv_glob])

    def tear_down(self):
        """実行後処理を行う."""
        super().tear_down()
