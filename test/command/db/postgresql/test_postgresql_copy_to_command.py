# -*- coding: utf-8 -*-

import os
import glob
import gzip
import filecmp
from ....abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.command.db.postgresql.postgresql_copy_to_command import PostgreSQLCopyToCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter

COMPONENT = Container().component('POSTGRESQL_COMPONENT.ID=UT')
TABLE_NAME = 'test_postgresql_copy_to_command'
TEST_DATA_DIR = 'test_data'


class TestPostgreSQLCopyToCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._sql_str = f'select * from {COMPONENT.schema}.{TABLE_NAME}'
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), TEST_DATA_DIR
            )
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        ShareParameter.dry_run_mode = False
        queue = CommandQueue()
        sql_str = f'drop table if exists {COMPONENT.schema}.{TABLE_NAME}'
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                sql_str.format(schema=COMPONENT.schema, table_name=TABLE_NAME))
        )
        sql_str = (
            'create table {schema}.{table_name} ('
            ' id integer,'
            ' str_column varchar(6),'
            ' date_column date'
            ');'
        )
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                sql_str.format(schema=COMPONENT.schema, table_name=TABLE_NAME)
            )
        )
        sql_str = (
            'insert into {schema}.{table_name} values'
            '(1, \'ABCDEF\', \'2020-04-01\'),'
            '(2, \'GHIJKL\', \'2020-04-01\'),'
            '(3, null, \'2020-04-01\');'
        )
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                sql_str.format(schema=COMPONENT.schema, table_name=TABLE_NAME)
            )
        )
        queue.execute()

    @classmethod
    def tearDownClass(cls) -> None:
        file_list = \
            glob.glob(
                os.path.join(
                    os.path.dirname(__file__), TEST_DATA_DIR, '*_for_assert.*'
                )
            )
        for file in file_list:
            os.remove(file)

    def test_copy_dry_run(self):
        ShareParameter.dry_run_mode = True
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['str_column', 'date_column']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()

    def test_copy_to_force_quoting_only_part(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_quoting_only_part_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_quoting_only_part.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['str_column', 'date_column']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_force_quoting_all(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_quoting_all_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_quoting_all.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['*']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_tsv(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_for_assert.tsv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command.tsv'
            )
        delimiter = '\t'
        null_str = None
        header = True
        quote = ' '
        escape = '"'
        gzip_mode = False
        force_quote_list = None
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_no_header(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_no_header_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_no_header.csv'
            )
        delimiter = ','
        null_str = None
        header = False
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['*']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_set_null_str(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_set_null_str_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_set_null_str.csv'
            )
        delimiter = ','
        null_str = '<NL>'
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['*']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_pip_delim(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_pip_delim_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_pip_delim.csv'
            )
        delimiter = '|'
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = False
        force_quote_list = ['*']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_no_quote(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_no_quote_for_assert.csv'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_no_quote.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = ' '
        escape = '\"'
        gzip_mode = False
        force_quote_list = None
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertTrue(filecmp.cmp(sample_csv_file_name, output_csv_file_name))

    def test_copy_to_gzip(self):
        ShareParameter.dry_run_mode = False
        output_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command_for_assert.csv.gz'
            )
        sample_csv_file_name = \
            os.path.join(
                self._test_data_path,
                'test_postgresql_copy_to_command.csv.gz'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        gzip_mode = True
        force_quote_list = ['str_column', 'date_column']
        encoding = 'utf8'
        command = PostgreSQLCopyToCommand(
            COMPONENT, self._sql_str, output_csv_file_name, delimiter,
            null_str, header, quote, escape, force_quote_list, encoding, gzip_mode
        )
        command.execute()
        self.assertEqual(
            gzip.open(output_csv_file_name, 'rt').read(),
            gzip.open(sample_csv_file_name, 'rt').read()
        )
