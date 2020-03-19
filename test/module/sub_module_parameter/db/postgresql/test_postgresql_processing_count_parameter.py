# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.db.postgresql.postgresql_processing_count_parameter import PostgreSQLProcessingCountParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestRedshiftProcessingCountParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._sql_file_name = \
            os.path.join(
                os.path.dirname(__file__),
                'sql',
                'test_postgresql_processing_count.sql'
            )
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = PostgreSQLProcessingCountParameter(
            {
                'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                'sql_file_name': self._sql_file_name,
                'assert_eq': 1,
                'assert_ne': 2,
                'assert_ge': 3,
                'assert_le': 4
            }
        )
        self.assertEqual('POSTGRESQL_COMPONENT.ID=UT', param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())
        self.assertEqual(1, param.assert_eq.get())
        self.assertEqual(2, param.assert_ne.get())
        self.assertEqual(3, param.assert_ge.get())
        self.assertEqual(4, param.assert_le.get())

    def test_must_parameter(self):
        param = PostgreSQLProcessingCountParameter(
            {
                'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                'sql_file_name': self._sql_file_name
            }
        )
        self.assertEqual('POSTGRESQL_COMPONENT.ID=UT', param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())

    def test_component_key_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'sql_file_name': self._sql_file_name
                }
            )

    def test_sql_file_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT'
                }
            )

    def test_sql_file_name_not_exists(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': 'not_exists.sql'
                }
            )

    def test_assert_eq_not_num(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': self._sql_file_name,
                    'assert_eq': 'a'
                }
            )

    def test_assert_ne_not_num(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': self._sql_file_name,
                    'assert_ne': 'a'
                }
            )

    def test_assert_ge_not_num(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': self._sql_file_name,
                    'assert_ge': 'a'
                }
            )

    def test_assert_le_not_num(self):
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingCountParameter(
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=UT',
                    'sql_file_name': self._sql_file_name,
                    'assert_le': 'a'
                }
            )
