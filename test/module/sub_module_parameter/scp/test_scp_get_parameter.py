# -*- coding: utf-8 -*-

from jetline.module.sub_module_parameter.scp.scp_get_parameter import ScpGetParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestScpGetParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = ScpGetParameter(
            {
                'scp_component_key': 'SCP_COMPONENT.ID=UT',
                'remote_path': '/tmp/remote/*',
                'local_dir_path': '/tmp/local',
                'recursive': True,
                'preserve_times': True
            }
        )
        self.assertEqual('SCP_COMPONENT.ID=UT', param.scp_component_key.get())
        self.assertEqual('/tmp/remote/*', param.remote_path.get())
        self.assertEqual('/tmp/local', param.local_dir_path.get())
        self.assertEqual(True, param.recursive.get())
        self.assertEqual(True, param.preserve_times.get())

    def test_must_parameter(self):
        param = ScpGetParameter(
            {
                'scp_component_key': 'SCP_COMPONENT.ID=UT',
                'remote_path': '/tmp/remote/*',
                'local_dir_path': '/tmp/local'
            }
        )
        self.assertEqual('SCP_COMPONENT.ID=UT', param.scp_component_key.get())
        self.assertEqual('/tmp/remote/*', param.remote_path.get())
        self.assertEqual('/tmp/local', param.local_dir_path.get())
        self.assertEqual(False, param.recursive.get())
        self.assertEqual(False, param.preserve_times.get())

    def test_component_key_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    'remote_path': '/tmp/remote/*',
                    'local_dir_path': '/tmp/local'
                }
            )

    def test_remote_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    'scp_component_key': 'SCP_COMPONENT.ID=UT',
                    'local_dir_path': '/tmp/local'
                }
            )

    def test_local_dir_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    'scp_component_key': 'SCP_COMPONENT.ID=UT',
                    'remote_path': '/tmp/remote/*'
                }
            )

    def test_recursive_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    'scp_component_key': 'SCP_COMPONENT.ID=UT',
                    'remote_path': '/tmp/remote/*',
                    'local_dir_path': '/tmp/local',
                    'recursive': 'not recursive'
                }
            )

    def test_preserve_times_not_bool(self):
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    'scp_component_key': 'SCP_COMPONENT.ID=UT',
                    'remote_path': '/tmp/remote/*',
                    'local_dir_path': '/tmp/local',
                    'preserve_times': 'none preserve_times'
                }
            )
