# -*- coding: utf-8 -*-

from jetline.module.sub_module_parameter.s3.s3_put_parameter import S3PutParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestS3PutParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = S3PutParameter(
            {
                's3_component_key': 'S3_COMPONENT.ID=UT',
                'local_file_path': 'test_source.csv',
                's3_dir_path': 'test_dir',
                'end_file_name': 'endfile'
            }
        )
        self.assertEqual('S3_COMPONENT.ID=UT', param.s3_component_key.get()),
        self.assertEqual('test_source.csv', param.local_file_path.get()),
        self.assertEqual('test_dir', param.s3_dir_path.get()),
        self.assertEqual('endfile', param.end_file_name.get()),

    def test_component_key_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter(
                {
                    'local_file_path': 'test_source.csv',
                    's3_dir_path': 'test_dir'
                }
            )

    def test_s3_dir_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter(
                {
                    's3_component_key': 'S3_COMPONENT.ID=UT',
                    'local_file_path': 'test_source.csv'
                }
            )
