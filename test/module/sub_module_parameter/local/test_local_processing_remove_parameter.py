# -*- coding: utf-8 -*-

from jetline.module.sub_module_parameter.local.local_processing_remove_parameter import LocalProcessingRemoveParameter
from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from test.abc.base_test_case import BaseTestCase


class TestLocalProcessingRemoveParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        param = LocalProcessingRemoveParameter(
            {
                'path_list': ['./test_target_01.csv', './test_target_02.csv'],
                'use_last_result': True,
            }
        )
        self.assertEqual(['./test_target_01.csv', './test_target_02.csv'], param.path_list.get()),
        self.assertEqual(True, param.use_last_result.get())

    def test_must_parameter(self):
        param = LocalProcessingRemoveParameter(
            {
                'path_list': ['./test_target_01.csv', './test_target_02.csv']
            }
        )
        self.assertEqual(['./test_target_01.csv', './test_target_02.csv'], param.path_list.get()),
        self.assertEqual(False, param.use_last_result.get())

    def test_path_list_not_list(self):
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingRemoveParameter(
                {
                    'path_list': {
                        'target_01': './test_target_01.csv',
                        'target_02': './test_target_02.csv'
                    }
                }
            )
