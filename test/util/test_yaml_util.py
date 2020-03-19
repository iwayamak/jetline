# -*- coding: utf-8 -*-

import os
from jetline.util.yaml_util import YamlUtil
from ..abc.base_test_case import BaseTestCase


class TestYamlUtil(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._test_data_dir = \
            os.path.join(
                os.path.dirname(__file__),
                'test_data'
            )
        super().__init__(*args, **kwargs)

    def test_load_file(self):
        yaml_name = \
            os.path.join(
                self._test_data_dir,
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

    def test_load_dir(self):
        y = YamlUtil.load_dir(self._test_data_dir)
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
        self.assertEqual(
            y['name'],'test_write_file'
        )
        self.assertEqual(
            y['value'][0]['param1'], 'value1'
        )
        self.assertEqual(
            y['value'][1]['param2'], 'value2'
        )

    def test_write_file(self):
        yaml_name = \
            os.path.join(
                self._test_data_dir,
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
        y = YamlUtil.load_file(yaml_name)
        self.assertEqual(
            y['name'], 'test_write_file'
        )
        self.assertEqual(
            y['value'][0]['param1'], 'value1'
        )
        self.assertEqual(
            y['value'][1]['param2'], 'value2'
        )
