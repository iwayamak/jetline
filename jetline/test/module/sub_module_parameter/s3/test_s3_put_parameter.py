# -*- coding: utf-8 -*-

from .....module.sub_module_parameter.s3.s3_put_parameter import S3PutParameter
from .....exception.sub_module_parameter_error import SubModuleParameterError
from .....test.abc.base_test_case import BaseTestCase


class TestS3Parameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = S3PutParameter(
            {
                's3_component_key': 'S3_COMPONENT.ID=UT',
                'file_path': 'test_source.csv',
                's3_dir_path': 'test_source.csv',
                'end_file_name': 'endfile'
            }
        )
        self.assertEqual('S3_COMPONENT.ID=UT', param.s3_component_key.get()),
        self.assertEqual('test_source.csv', param.file_path.get()),
        self.assertEqual('test_source.csv', param.s3_dir_path.get()),
        self.assertEqual('endfile', param.end_file_name.get()),

    def test_component_key_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter(
                {
                    'file_path': 'test_source.csv',
                    's3_dir_path': 'test_source.csv'
                }
            )

    def test_s3_dir_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter(
                {
                    's3_component_key': 'S3_COMPONENT.ID=UT',
                    'file_path': 'test_source.csv'
                }
            )
