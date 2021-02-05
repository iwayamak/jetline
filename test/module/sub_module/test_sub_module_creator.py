# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from jetline.module.sub_module.sub_module_creator import SubModuleCreator
from jetline.module.sub_module_parameter.db.postgresql.postgresql_processing_parameter import PostgreSQLProcessingParameter
from jetline.module.sub_module_parameter.db.postgresql.postgresql_processing_count_parameter import PostgreSQLProcessingCountParameter
from jetline.module.sub_module.db.postgresql.postgresql_processing import PostgreSQLProcessing
from jetline.module.sub_module.db.postgresql.postgresql_processing_count import PostgreSQLProcessingCount


class TestSubModuleCreator(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._sql_file_name = \
            os.path.join(
                os.path.dirname(__file__), 'test_sub_module_creator.sql'
            )
        super().__init__(*args, **kwargs)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_sub_module(self):
        # modeなし
        sub_module = \
            SubModuleCreator.create_sub_module(
                'PostgreSQLProcessing',
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT',
                    'sql_file_name': self._sql_file_name
                }
            )
        self.assertIsInstance(sub_module, PostgreSQLProcessing)
        self.assertIsInstance(sub_module._parameter, PostgreSQLProcessingParameter)

    def test_create_sub_module_set_mode(self):
        sub_module = \
            SubModuleCreator.create_sub_module(
                'PostgreSQLProcessing',
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT',
                    'sql_file_name': self._sql_file_name,
                    'assert_eq': 3
                },
                'Count'
            )
        self.assertIsInstance(sub_module, PostgreSQLProcessingCount)
        self.assertIsInstance(sub_module._parameter, PostgreSQLProcessingCountParameter)

    def test_create_sub_module_list(self):
        sub_module_list = \
            SubModuleCreator.create_sub_module(
                'PostgreSQLProcessing',
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT',
                    'sql_file_name': self._sql_file_name
                }
            )
        self.assertIsInstance(sub_module_list, PostgreSQLProcessing)
        self.assertIsInstance(sub_module_list._parameter, PostgreSQLProcessingParameter)

    def test_create_sub_module_list_set_mode(self):
        sub_module = \
            SubModuleCreator.create_sub_module(
                'PostgreSQLProcessing',
                {
                    'postgresql_component_key': 'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT',
                    'sql_file_name': self._sql_file_name,
                    'assert_eq': 3
                },
                'Count'
            )
        self.assertIsInstance(sub_module, PostgreSQLProcessingCount)
        self.assertIsInstance(sub_module._parameter, PostgreSQLProcessingCountParameter)
