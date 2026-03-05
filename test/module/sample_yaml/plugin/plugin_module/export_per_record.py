"""1レコード単位でファイル出力する PostgreSQL サンプルコマンド."""

import logging
import os

from jetline.command.db.postgresql.abc.postgresql_command import PostgreSQLCommand
from jetline.container.container import Container
from jetline.util.file_util import FileUtil

logger = logging.getLogger("jetline")


class ExportPerRecord(PostgreSQLCommand):
    """クエリ結果をレコードごとに個別ファイルへ書き出すコマンド."""

    def __init__(self, kwargs: dict):
        """入力引数から実行設定を構築する.

        Args:
            kwargs: `component_key`、`sql_file_name`、`output_dir` を含む設定.
        """
        component = Container.component(kwargs["component_key"])
        sql_str = FileUtil.file_to_str(kwargs["sql_file_name"])
        self._output_dir = kwargs["output_dir"]
        super().__init__(component, sql_str)

    def set_up(self) -> None:
        """出力ディレクトリを準備する."""
        super().set_up()
        os.makedirs(self._output_dir, exist_ok=True)

    def body(self) -> None:
        """メイン処理のフックを呼び出す."""
        super().body()

    def run(self) -> None:
        """クエリ結果を重複回避しながらファイル出力する."""
        super().run()
        self._cursor = self._connection.cursor(name="server_cursor")
        self._cursor.execute(self._query)

        uniq_check_list: list[str] = []
        for row in self._cursor:
            base_name = row[0]
            if base_name in uniq_check_list:
                file_base_name, ext = os.path.splitext(base_name)
                file_name = os.path.join(
                    self._output_dir,
                    f"{file_base_name}_{uniq_check_list.count(base_name)}{ext}",
                )
            else:
                file_name = os.path.join(self._output_dir, base_name)

            FileUtil.str_to_file(file_name, row[1])
            uniq_check_list.append(base_name)

    def dry_run(self) -> None:
        """Dry-run 時のフックを呼び出す."""
        super().dry_run()

    def tear_down(self) -> None:
        """後処理のフックを呼び出す."""
        super().tear_down()
