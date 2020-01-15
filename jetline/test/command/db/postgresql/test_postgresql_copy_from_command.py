# -*- coding: utf-8 -*-

import os
import sys
from ....abc.base_test_case import BaseTestCase
from .....command.command_queue import CommandQueue
from .....command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from .....command.db.postgresql.postgresql_copy_from_command import PostgreSQLCopyFromCommand
from .....container.container import Container
from .....share_parameter.share_parameter import ShareParameter

COMPONENT = Container().component('POSTGRESQL_COMPONENT.ID=UT')
TABLE_NAME = 'test_postgresql_copy_from_command'
TEST_DATA_DIR = 'test_data'


class TestPostgreSQLCopyFromCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), TEST_DATA_DIR
            )
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        ShareParameter.dry_run_mode = False
        queue = CommandQueue()
        sql_str = 'drop table if exists {schema}.{table_name}'
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
        queue.execute()

    def test_copy_from_dry_run(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = True
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null_str, header, quote, escape
        )
        command.execute()

    def test_copy_from(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.csv'
            )
        delimiter = ','
        null_str = None
        header = True
        quote = '"'
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null_str, header, quote, escape
        )
        command.execute()

    def test_copy_from_tsv(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command.tsv'
            )
        delimiter = '\t'
        null_str = None
        header = True
        quote = ' '
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null_str, header, quote, escape
        )
        command.execute()

    def test_copy_from_no_header(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_no_header.csv'
            )
        delimiter = ','
        null_str = None
        header = False
        quote = '"'
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null_str, header, quote, escape
        )
        command.execute()

    def test_copy_from_set_null_str(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_set_null_str.csv'
            )
        delimiter = ','
        null = '<NL>'
        header = True
        quote = '"'
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null, header, quote, escape
        )
        command.execute()

    def test_copy_from_pip_delim(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = \
            os.path.join(
                self._test_data_path, 'test_postgresql_copy_from_command_pipe_delim.csv'
            )
        delimiter = '|'
        null = None
        header = True
        quote = '"'
        escape = '"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null, header, quote, escape
        )
        command.execute()

    def test_copy_from_no_quote(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        csv_file_name = os.path.join(
            self._test_data_path, 'test_postgresql_copy_from_command_no_quote.csv'
        )
        delimiter = ','
        null = None
        header = True
        quote = ' '
        escape = '\"'
        command = PostgreSQLCopyFromCommand(
            COMPONENT, TABLE_NAME, csv_file_name, delimiter, null, header, quote, escape
        )
        command.execute()
