"""FileUtil のユニットテスト。."""

import os

from jetline.util.file_util import FileUtil
from test.abc.base_test_case import BaseTestCase


class TestFileUtil(BaseTestCase):
    """FileUtil の入出力・変換処理を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_file_to_str(self):
        """ファイル内容を文字列として取得できることを確認する。."""
        filename = os.path.join(os.path.dirname(__file__), "test_file_util.txt")
        content = FileUtil.file_to_str(filename)
        self.assertEqual(content, "text_file_util用テストファイル")

    def test_str_to_file(self):
        """文字列をファイルへ上書きできることを確認する。."""
        filename = os.path.join(os.path.dirname(__file__), "test_file_util_write.txt")
        FileUtil.str_to_file(filename, "test_str_to_file")
        content = FileUtil.file_to_str(filename)
        self.assertEqual(content, "test_str_to_file")

    def test_str_to_file_append(self):
        """文字列追記が正しく行えることを確認する。."""
        filename = os.path.join(os.path.dirname(__file__), "test_file_util_write_a.txt")
        FileUtil.str_to_file(filename, "test_str_to_file")
        FileUtil.str_to_file_append(filename, "test_str_to_file_append")
        content = FileUtil.file_to_str(filename)
        self.assertEqual(content, "test_str_to_filetest_str_to_file_append")

    def test_tsv_to_html_table(self):
        """TSV から HTML テーブルへ変換できることを確認する。."""
        filename = os.path.join(os.path.dirname(__file__), "test_file_util.tsv")
        column = "\t".join(["column1", "column2"]) + "\n"
        html_table = FileUtil.tsv_str_to_html_table(FileUtil.file_to_str(filename), column)
        self.assertEqual(
            "<table><tr><td>column1</td><td>column2</td></tr><tr><td>1</td><td>foo</td></tr></table>",
            html_table,
        )
