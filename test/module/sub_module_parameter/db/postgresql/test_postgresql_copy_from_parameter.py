# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.db.postgresql.postgresql_copy_from_parameter import PostgreSQLCopyFromParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestPostgreSQLCopyFromParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._csv_file_name = \
            os.path.join(
                os.path.dirname(__file__),
                'test_data',
                'test_postgresql_copy_from_parameter.csv'
            )
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = PostgreSQLCopyFromParameter(
            {
                'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                'table_name': 'test_postgresql_copy_from_parameter_table',
                'column_list': ['column_1, column_2, column_3'],
                'csv_file_name': self._csv_file_name,
                'delimiter': '\t',
                'null_str': '<NL>',
                'header': False,
                'quote': ' ',
                'escape': '\t',
                'encoding': 'sjis',
                'gzip': False,
                'remove_source_file': True
            }
        )
        self.assertEqual('POSTGRESQL_COMPONENT.ID=UT', param.postgresql_component_key.get())
        self.assertEqual('test_postgresql_copy_from_parameter_table', param.table_name.get())
        self.assertEqual(['column_1, column_2, column_3'], param.column_list.get())
        self.assertEqual(self._csv_file_name, param.csv_file_name.get())
        self.assertEqual('\t', param.delimiter.get())
        self.assertEqual('<NL>', param.null_str.get())
        self.assertEqual(False, param.header.get())
        self.assertEqual(' ', param.quote.get())
        self.assertEqual('\t', param.escape.get())
        self.assertEqual('sjis', param.encoding.get())
        self.assertEqual(False, param.gzip.get())
        self.assertEqual(True, param.remove_source_file.get())

    def test_must_parameter(self):
        param = PostgreSQLCopyFromParameter(
            {
                'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                'table_name': 'test_postgresql_copy_from_parameter_table',
                'csv_file_name': self._csv_file_name
            }
        )
        self.assertEqual('POSTGRESQL_COMPONENT.ID=UT', param.postgresql_component_key.get())
        self.assertEqual('test_postgresql_copy_from_parameter_table', param.table_name.get())
        self.assertEqual(None, param.column_list.get())
        self.assertEqual(self._csv_file_name, param.csv_file_name.get())
        self.assertEqual(',', param.delimiter.get())
        self.assertEqual(None, param.null_str.get())
        self.assertEqual(True, param.header.get())
        self.assertEqual('"', param.quote.get())
        self.assertEqual('"', param.escape.get())
        self.assertEqual('utf8', param.encoding.get())
        self.assertEqual(False, param.gzip.get())
        self.assertEqual(False, param.remove_source_file.get())

    def test_component_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'table_name': 'test_postgresql_copy_from_parameter_table',
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_table_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_column_list_not_list(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'table_name': 'test_postgresql_copy_from_parameter_table',
                    'column_list': 'column_1',
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_header_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'table_name': 'test_postgresql_copy_from_parameter_table',
                    'csv_file_name': self._csv_file_name,
                    'header': 'header exists'
                }
            )

    def test_gzip_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'table_name': 'test_postgresql_copy_from_parameter_table',
                    'csv_file_name': self._csv_file_name,
                    'gzip': 'gzip'
                }
            )

    def test_remove_source_file_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyFromParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'table_name': 'test_postgresql_copy_from_parameter_table',
                    'csv_file_name': self._csv_file_name,
                    'remove_source_file': 'remove'
                }
            )
