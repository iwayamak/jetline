# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.db.postgresql.postgresql_copy_to_parameter import PostgreSQLCopyToParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestPostgreSQLCopyToParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = 'POSTGRESQL_COMPONENT.ID=UT'
        self._csv_file_name = 'test_postgresql_copy_to_parameter.csv'
        self._sql_file_name = \
            os.path.join(
                os.path.dirname(__file__),
                'sql',
                'test_postgresql_copy_to_parameter.sql'
            )
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = PostgreSQLCopyToParameter(
            {
                'postgresql_component_key': self._component,
                'sql_file_name': self._sql_file_name,
                'csv_file_name': self._csv_file_name,
                'delimiter': '\t',
                'null_str': '<NL>',
                'header': False,
                'quote': ' ',
                'escape': '\t',
                'gzip': True,
                'force_quote_list': ['*'],
                'encoding': 'sjis'
            }
        )
        self.assertEqual(self._component, param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())
        self.assertEqual(self._csv_file_name, param.csv_file_name.get())
        self.assertEqual('\t', param.delimiter.get())
        self.assertEqual('<NL>', param.null_str.get())
        self.assertEqual(False, param.header.get())
        self.assertEqual(' ', param.quote.get())
        self.assertEqual('\t', param.escape.get())
        self.assertEqual(True, param.gzip.get())
        self.assertEqual(['*'], param.force_quote_list.get())
        self.assertEqual('sjis', param.encoding.get())

    def test_must_parameter(self):
        param = PostgreSQLCopyToParameter(
            {
             'postgresql_component_key': self._component,
             'sql_file_name': self._sql_file_name,
             'csv_file_name': self._csv_file_name
            }
        )
        self.assertEqual(self._component, param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())
        self.assertEqual(self._csv_file_name, param.csv_file_name.get())
        self.assertEqual(',', param.delimiter.get())
        self.assertEqual(None, param.null_str.get())
        self.assertEqual(True, param.header.get())
        self.assertEqual('"', param.quote.get())
        self.assertEqual('"', param.escape.get())
        self.assertEqual(False, param.gzip.get())
        self.assertEqual(None, param.force_quote_list.get())
        self.assertEqual('utf-8', param.encoding.get())

    def test_component_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'sql_file_name': self._sql_file_name,
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_sql_file_name_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_sql_file_name_name_not_exists(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'sql_file_name': 'not_exists.sql',
                    'csv_file_name': self._csv_file_name
                }
            )

    def test_csv_file_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'sql_file_name': self._sql_file_name
                }
            )

    def test_header_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'sql_file_name': self._sql_file_name,
                    'csv_file_name': self._csv_file_name,
                    'header': 'header exists'
                }
            )

    def test_force_quote_list_not_list(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'sql_file_name': self._sql_file_name,
                    'csv_file_name': self._csv_file_name,
                    'force_quote_list': '*'
                }
            )

    def test_gzip_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLCopyToParameter(
                {
                    'postgresql_component_key': self._component,
                    'sql_file_name': self._sql_file_name,
                    'csv_file_name': self._csv_file_name,
                    'gzip': 'gzip'
                }
            )
