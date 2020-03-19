# -*- coding: utf-8 -*-

import os
from jetline.module.sub_module_parameter.plugin_parameter import PluginParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from ...abc.base_test_case import BaseTestCase


class TestPluginParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = PluginParameter(
            {
                'plugin_path': self._plugin_path,
                'package': 'sample_command',
                'class_name': 'SampleCommand',
                'kwargs': {'key1': 'value1'}
            }
        )
        self.assertEqual(self._plugin_path, param.plugin_path.get())
        self.assertEqual('sample_command', param.package.get()),
        self.assertEqual('SampleCommand', param.class_name.get()),
        self.assertEqual({'key1': 'value1'}, param.kwargs.get())

    def test_must_parameter(self):
        param = PluginParameter(
            {
                'plugin_path': self._plugin_path,
                'package': 'sample_command',
                'class_name': 'SampleCommand'
            }
        )
        self.assertEqual(self._plugin_path, param.plugin_path.get())
        self.assertEqual('sample_command', param.package.get()),
        self.assertEqual('SampleCommand', param.class_name.get()),

    def test_plugin_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    'package': 'sample_command.py',
                    'class_name': 'SampleCommand'
                }
            )

    def test_plugin_path_not_exists(self):
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    'plugin_path': os.path.join(os.path.dirname(__file__), 'plugins2'),
                    'package': 'sample_command.py',
                    'class_name': 'SampleCommand'
                }
            )

    def test_package_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    'plugin_path': self._plugin_path,
                    'class_name': 'SampleCommand'
                }
            )

    def test_class_name_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    'plugin_path': self._plugin_path,
                    'package': 'sample_command.py'
                }
            )

    def test_kwargs_not_dict(self):
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    'plugin_path': self._plugin_path,
                    'kwargs': '1'
                }
            )
