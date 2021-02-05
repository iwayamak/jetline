# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.db.postgresql.postgresql_processing_parameter import PostgreSQLProcessingParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestRedshiftProcessingParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._sql_file_name = \
            os.path.join(
                os.path.dirname(__file__),
                'sql',
                'test_postgresql_processing.sql'
            )
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = PostgreSQLProcessingParameter(
            {
                'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                'sql_file_name': self._sql_file_name
            }
        )
        self.assertEqual('POSTGRESQL_COMPONENT.ID=UT', param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())

    def test_component_key_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter(
                {
                    'sql_file_name': self._sql_file_name
                }
            )

    def test_sql_filename_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT'
                }
            )

    def test_sql_file_not_exists(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': 'not_exists.sql'
                }
            )
