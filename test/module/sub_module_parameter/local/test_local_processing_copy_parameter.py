# -*- coding: utf-8 -*-

from jetline.module.sub_module_parameter.local.local_processing_copy_parameter import LocalProcessingCopyParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestLocalProcessingCopyParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = LocalProcessingCopyParameter(
            {
                'source_path': './test_source.csv',
                'destination_path': './test_destination.csv'
            }
        )
        self.assertEqual('./test_source.csv', param.source_path.get()),
        self.assertEqual('./test_destination.csv', param.destination_path.get()),

    def test_source_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingCopyParameter(
                {
                    'destination_path': './test_destination.csv'
                }
            )

    def test_destination_path_not_set(self):
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingCopyParameter(
                {
                    'source_path': './test_source.csv',
                }
            )
