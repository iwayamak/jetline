# -*- coding: utf-8 -*-

import os
from unittest import TestCase
from ...util.yaml_util import YamlUtil


class TestYamlUtil(TestCase):
    def test_load_file(self):
        yaml_name = \
            os.path.join(
                os.path.dirname(__file__),
                'test_yaml_util.yaml'
            )
        y = YamlUtil.load_file(yaml_name)
        sub_module = y['sub_module'][0]
        self.assertEqual(
            sub_module['name'], 'PostgreSQLProcessing'
        )
        param = sub_module['param']
        self.assertEqual(
            param['postgresql_component_key'],
            'POSTGRESQL_COMPONENT.ID=UT'
        )
        self.assertEqual(
            param['sql_file_name'],
            'test_postgresql_processing.sql'
        )

    def test_write_file(self):
        yaml_name = \
            os.path.join(
                os.path.dirname(__file__),
                'test_yaml_util_write.yaml'
            )
        y = \
            {
                'name': 'test_write_file',
                'value': [
                    {'param1': 'value1'},
                    {'param2': 'value2'}
                ]
            }
        YamlUtil.write_file(yaml_name, y)
