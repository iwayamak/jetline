"""PostgreSQLCopyToCommand のユニットテスト."""

import filecmp
import glob
import gzip
import os

from jetline.command.command_queue import CommandQueue
from jetline.command.db.postgresql.postgresql_copy_to_command import PostgreSQLCopyToCommand
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase

COMPONENT = Container().component("POSTGRESQL_COMPONENT.ID=UT")
TABLE_NAME = "test_postgresql_copy_to_command"
TEST_DATA_DIR = "test_data"


class TestPostgreSQLCopyToCommand(BaseTestCase):
    """PostgreSQLCopyToCommand の出力バリエーションを検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._sql_str = f"select * from {COMPONENT.schema}.{TABLE_NAME}"
        self._test_data_path = os.path.join(os.path.dirname(__file__), TEST_DATA_DIR)
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        """テストテーブルを初期化する."""
        ShareParameter.dry_run_mode = False
        queue = CommandQueue()
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                f"drop table if exists {COMPONENT.schema}.{TABLE_NAME}",
            )
        )
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                (
                    f"create table {COMPONENT.schema}.{TABLE_NAME} ("
                    " id integer,"
                    " str_column varchar(6),"
                    " date_column date"
                    ");"
                ),
            )
        )
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                (
                    f"insert into {COMPONENT.schema}.{TABLE_NAME} values"
                    "(1, 'ABCDEF', '2020-04-01'),"
                    "(2, 'GHIJKL', '2020-04-01'),"
                    "(3, null, '2020-04-01');"
                ),
            )
        )
        queue.execute()

    @classmethod
    def tearDownClass(cls) -> None:
        """アサート用に生成したファイルを削除する."""
        file_list = glob.glob(
            os.path.join(os.path.dirname(__file__), TEST_DATA_DIR, "*_for_assert.*")
        )
        for file in file_list:
            os.remove(file)

    def _execute_copy(
        self,
        output_file_name: str,
        delimiter: str,
        null_str: str | None,
        header: bool,
        quote: str,
        escape: str,
        force_quote_list: list[str] | None,
        encoding: str,
        gzip_mode: bool,
    ):
        """COPY TO コマンドを実行する."""
        command = PostgreSQLCopyToCommand(
            COMPONENT,
            self._sql_str,
            output_file_name,
            delimiter,
            null_str,
            header,
            quote,
            escape,
            force_quote_list,
            encoding,
            gzip_mode,
        )
        command.execute()

    def test_copy_dry_run(self):
        """Dry-run で例外なく実行できることを確認する."""
        ShareParameter.dry_run_mode = True
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command.csv",
        )
        self._execute_copy(
            output_csv_file_name,
            ",",
            None,
            True,
            '"',
            '"',
            ["str_column", "date_column"],
            "utf8",
            False,
        )

    def test_copy_to_force_quoting_only_part(self):
        """一部カラム強制クォート出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_quoting_only_part_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_quoting_only_part.csv",
        )
        self._execute_copy(
            output_csv_file_name,
            ",",
            None,
            True,
            '"',
            '"',
            ["str_column", "date_column"],
            "utf8",
            False,
        )
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_force_quoting_all(self):
        """全カラム強制クォート出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_quoting_all_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_quoting_all.csv",
        )
        self._execute_copy(output_csv_file_name, ",", None, True, '"', '"', ["*"], "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_tsv(self):
        """TSV 出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_for_assert.tsv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command.tsv",
        )
        self._execute_copy(output_csv_file_name, "\t", None, True, " ", '"', None, "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_no_header(self):
        """ヘッダー無し出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_no_header_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_no_header.csv",
        )
        self._execute_copy(output_csv_file_name, ",", None, False, '"', '"', ["*"], "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_set_null_str(self):
        """NULL 置換文字列出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_set_null_str_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_set_null_str.csv",
        )
        self._execute_copy(output_csv_file_name, ",", "<NL>", True, '"', '"', ["*"], "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_pip_delim(self):
        """区切り文字 `|` 出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_pip_delim_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_pip_delim.csv",
        )
        self._execute_copy(output_csv_file_name, "|", None, True, '"', '"', ["*"], "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_no_quote(self):
        """クォート無し出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_no_quote_for_assert.csv",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_no_quote.csv",
        )
        self._execute_copy(output_csv_file_name, ",", None, True, " ", '"', None, "utf8", False)
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_gzip(self):
        """Gzip 出力を確認する."""
        ShareParameter.dry_run_mode = False
        output_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command_for_assert.csv.gz",
        )
        sample_csv_file_name = os.path.join(
            self._test_data_path,
            "test_postgresql_copy_to_command.csv.gz",
        )
        self._execute_copy(
            output_csv_file_name,
            ",",
            None,
            True,
            '"',
            '"',
            ["str_column", "date_column"],
            "utf8",
            True,
        )
        with gzip.open(output_csv_file_name, "rt") as output_fp:
            output_text = output_fp.read()
        with gzip.open(sample_csv_file_name, "rt") as sample_fp:
            sample_text = sample_fp.read()
        self.assertEqual(output_text, sample_text)
