# -*- coding: utf-8 -*-

import sys
from ....abc.base_test_case import BaseTestCase
from .....module.sub_module.result.sub_module_result import SubModuleResult
from .....share_parameter.share_parameter import ShareParameter


class TestSubModuleResult(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._result = None
        super().__init__(*args, **kwargs)

    def setUp(self):
        self._result = SubModuleResult()

    def test_get_last_log_no_data(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        self.assertIsNone(self._result.get_last_log_sub_module_name())
        self.assertIsNone(self._result.get_last_log_processing_time())
        self.assertIsNone(self._result.get_last_log_status())
        self.assertIsNone(self._result.get_last_log_start_time())
        self.assertIsNone(self._result.get_last_log_end_time())
        self.assertIsNone(self._result.get_last_log_data_file())
        self.assertIsNone(self._result.get_last_log_local_data_file_list())
        self.assertIsNone(self._result.get_last_log_s3_data_file_list())

    def test_get_last_log_no_data_file_list(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        self._result.append_result('test_sub_module1', '2015-02-06 15:12:25,123', '2015-02-06 15:12:26,123', 1.0)
        self.assertEqual('test_sub_module1', self._result.get_last_log_sub_module_name())
        self.assertEqual(1.0, self._result.get_last_log_processing_time())
        self.assertEqual('success', self._result.get_last_log_status())
        self.assertEqual('2015-02-06 15:12:25,123', self._result.get_last_log_start_time())
        self.assertEqual('2015-02-06 15:12:26,123', self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual(0, len(self._result.get_last_log_local_data_file_list()))
        self.assertEqual(0, len(self._result.get_last_log_s3_data_file_list()))

    def test_get_last_log_exists_single_data_flie_list(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        self._result.append_result('test_sub_module2', '2015-02-06 16:12:25,123', '2015-02-06 16:12:26,123', 2.0,
                                   status='error', local_data_file_list=['test1.txt'], s3_data_file_list=['test2.txt'])
        self.assertEqual('test_sub_module2', self._result.get_last_log_sub_module_name())
        self.assertEqual(2.0, self._result.get_last_log_processing_time())
        self.assertEqual('error', self._result.get_last_log_status())
        self.assertEqual('2015-02-06 16:12:25,123', self._result.get_last_log_start_time())
        self.assertEqual('2015-02-06 16:12:26,123', self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual('test1.txt', self._result.get_last_log_local_data_file_list()[0])
        self.assertEqual('test2.txt', self._result.get_last_log_s3_data_file_list()[0])

    def test_get_last_log_exists_multiple_data_file_list(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        self._result.append_result('test_sub_module3', '2015-02-06 17:12:25,123', '2015-02-06 17:12:26,123', 3.0,
                                   status='success', local_data_file_list=['test21.txt', 'test22.txt'],
                                   s3_data_file_list=['test31.txt', 'test32.txt'])
        self.assertEqual('test_sub_module3', self._result.get_last_log_sub_module_name())
        self.assertEqual(3.0, self._result.get_last_log_processing_time())
        self.assertEqual('success', self._result.get_last_log_status())
        self.assertEqual('2015-02-06 17:12:25,123', self._result.get_last_log_start_time())
        self.assertEqual('2015-02-06 17:12:26,123', self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual('test21.txt', self._result.get_last_log_local_data_file_list()[0])
        self.assertEqual('test22.txt', self._result.get_last_log_local_data_file_list()[1])
        self.assertEqual('test31.txt', self._result.get_last_log_s3_data_file_list()[0])
        self.assertEqual('test32.txt', self._result.get_last_log_s3_data_file_list()[1])
