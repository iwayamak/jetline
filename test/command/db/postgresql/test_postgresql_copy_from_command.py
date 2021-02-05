# -*- coding: utf-8 -*-

import os
from ....abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter

COMPONENT = Container().component('POSTGRESQL_COMPONENT.ID=UT')
TABLE_NAME = f'{COMPONENT.schema}.test_postgresql_copy_from_command'
TEST_DATA_DIR = 'test_data'


class TestPostgreSQLCopyFromCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), TEST_DATA_DIR
            )
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        ShareParameter.dry_run_mode = False
        queue = CommandQueue()
        sql_str = 'drop table if exists {table_name}'
        queue.add_command(
            PostgreSQLProcessingCommand(
                COMPONENT,
                sql_str.format(schema=COMPONENT.schema, table_name=TABLE_NAME))
        )
        sql_str = (
            'create table {table_name} ('
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
        queue.execute()

    def test_copy_from_dry_run(self):
        ShareParameter.dry_run_mode = True
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_set_column_list(self):
        ShareParameter.dry_run_mode = False
        column_list = ['id', 'str_column', 'date_column']
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_tsv(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.tsv'
            )
        delimiter = '\t'
        null_str = None
        header = True
        quote = ' '
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_no_header(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_no_header.csv'
            )
        delimiter = ','
        null_str = None
        header = False
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_set_null_str(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_set_null_str.csv'
            )
        delimiter = ','
        null = '<NL>'
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_pip_delim(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_pipe_delim.csv'
            )
        delimiter = '|'
        null = None
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_no_quote(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = os.path.join(
            self._test_data_path, 'test_postgresql_copy_from_command_no_quote.csv'
        )
        delimiter = ','
        null = None
        header = True
        quote = ' '
        escape = '\"'
        encoding = 'utf8'
        gzip = False
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null, header, quote, escape, encoding, gzip
        )
        command.execute()

    def test_copy_from_gzip(self):
        ShareParameter.dry_run_mode = False
        column_list = None
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv.gz'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        encoding = 'utf8'
        gzip = True
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, column_list, [csv_file_name], delimiter,
            null_str, header, quote, escape, encoding, gzip
        )
        command.execute()
