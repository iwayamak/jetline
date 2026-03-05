"""PostgreSQLCopyFromCommand のユニットテスト."""

import os

from jetline.command.command_queue import CommandQueue
from jetline.command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter

from ....abc.base_test_case import BaseTestCase

COMPONENT = Container().component("POSTGRESQL_COMPONENT.ID=UT")
TABLE_NAME = f"{COMPONENT.schema}.test_postgresql_copy_from_command"
TEST_DATA_DIR = "test_data"


class TestPostgreSQLCopyFromCommand(BaseTestCase):
    """PostgreSQLCopyFromCommand の各種入力条件を検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._test_data_path = os.path.join(os.path.dirname(__file__), TEST_DATA_DIR)
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        """検証用テーブルを作成する."""
        ShareParameter.dry_run_mode = False
        queue = CommandQueue()
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                f"drop table if exists {TABLE_NAME}",
            )
        )
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                (
                    f"create table {TABLE_NAME} ("
                    " id integer,"
                    " str_column varchar(6),"
                    " date_column date"
                    ");"
                ),
            )
        )
        queue.execute()

    def _run_copy_from(
        self,
        file_name: str,
        delimiter: str = ",",
        null_str: str | None = None,
        header: bool = True,
        quote: str = '"',
        escape: str = '"',
        encoding: str = "utf8",
        gzip_mode: bool = False,
        column_list: list[str] | None = None,
    ) -> None:
        """共通設定で COPY FROM コマンドを実行する.

        Args:
            file_name: 読み込む入力ファイル名.
            delimiter: 区切り文字.
            null_str: NULL 文字列表現.
            header: ヘッダー行を含むかどうか.
            quote: クォート文字.
            escape: エスケープ文字.
            encoding: 文字コード.
            gzip_mode: Gzip 圧縮ファイルとして読むかどうか.
            column_list: 取り込み対象カラムの並び.
        """
        command = PostgreSQLCopyFromCommand(
            COMPONENT,
            TABLE_NAME,
            column_list,
            [os.path.join(self._test_data_path, file_name)],
            delimiter,
            null_str,
            header,
            quote,
            escape,
            encoding,
            gzip_mode,
        )
        command.execute()

    def test_copy_from_dry_run(self) -> None:
        """Dry-run でも例外なく実行できることを確認する."""
        ShareParameter.dry_run_mode = True
        self._run_copy_from("test_postgresql_copy_from_command.csv")

    def test_copy_from(self) -> None:
        """標準 CSV を取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from("test_postgresql_copy_from_command.csv")

    def test_copy_from_set_column_list(self) -> None:
        """カラム指定ありで取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command.csv",
            column_list=["id", "str_column", "date_column"],
        )

    def test_copy_from_tsv(self) -> None:
        """TSV 形式の取り込みを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command.tsv",
            delimiter="\t",
            quote=" ",
        )

    def test_copy_from_no_header(self) -> None:
        """ヘッダー無し CSV を取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command_no_header.csv",
            header=False,
        )

    def test_copy_from_set_null_str(self) -> None:
        """NULL 置換文字列指定で取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command_set_null_str.csv",
            null_str="<NL>",
        )

    def test_copy_from_pip_delim(self) -> None:
        """区切り文字 `|` の入力を取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command_pipe_delim.csv",
            delimiter="|",
        )

    def test_copy_from_no_quote(self) -> None:
        """クォート無し形式を取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command_no_quote.csv",
            quote=" ",
            escape='\\"',
        )

    def test_copy_from_gzip(self) -> None:
        """Gzip 圧縮 CSV を取り込めることを確認する."""
        ShareParameter.dry_run_mode = False
        self._run_copy_from(
            "test_postgresql_copy_from_command.csv.gz",
            gzip_mode=True,
        )
