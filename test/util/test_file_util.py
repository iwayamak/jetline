# -*- coding: utf-8 -*-

import os
from ..abc.base_test_case import BaseTestCase
from jetline.util.file_util import FileUtil


class TestFileUtil(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_file_to_str(self):
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_file_util.txt'
            )
        file = FileUtil.file_to_str(filename)
        self.assertEqual(file, 'text_file_util用テストファイル')

    def test_str_to_file(self):
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_file_util_write.txt'
            )
        FileUtil.str_to_file(filename, 'test_str_to_file')
        file = FileUtil.file_to_str(filename)
        self.assertEqual(file, 'test_str_to_file')

    def test_str_to_file_append(self):
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_file_util_write_a.txt'
            )
        FileUtil.str_to_file(filename, 'test_str_to_file')
        FileUtil.str_to_file_append(
            filename, 'test_str_to_file_append'
        )
        file = FileUtil.file_to_str(filename)
        self.assertEqual(
            file, 'test_str_to_filetest_str_to_file_append'
        )

    def test_tsv_to_html_table(self):
        filename = \
            os.path.join(
                os.path.dirname(__file__),
                'test_file_util.tsv'
            )
        column = '\t'.join(['column1', 'column2']) + '\n'
        html_table = \
            FileUtil.tsv_str_to_html_table(
                FileUtil.file_to_str(filename), column
            )
        self.assertEqual(
            '<table><tr><td>column1</td><td>column2</td></tr><tr><td>1</td><td>foo</td></tr></table>',
            html_table
        )
