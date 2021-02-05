# -*- coding: utf-8 -*-

import datetime
import logging
from typing import Union
from ....share_parameter.share_parameter import ShareParameter

logger = logging.getLogger('jetline')


class SubModuleResult(object):
    FILE_NAME_SUFFIX = '_result.yaml'
    KEY_SETTINGS_YAML_RESULT_DIR = 'result_dir'
    KEY_BATCH_NAME = 'batch_name'
    KEY_LOG = 'log'
    KEY_SUB_MODULE_NAME = 'sub_module_name'
    KEY_DATA_FILE = 'data_file'
    KEY_DATA_FILE_S3 = 's3'
    KEY_DATA_FILE_LOCAL = 'local'
    KEY_STATUS = 'status'
    KEY_UPDATE_TS = 'update_ts'
    KEY_START_TIME = 'start_time'
    KEY_END_TIME = 'end_time'
    KEY_PROCESSING_TIME = 'processing_time'
    C_COMPONENT = 'c_component'
    C_TABLE_NAME = 'c_table_name'
    C_COLUMNS = 'c_columns'
    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'

    def __init__(self):
        self._param = None
        self._param = dict()
        self._param[self.KEY_BATCH_NAME] = ShareParameter.batch_name
        self._param[self.KEY_LOG] = []

    def append_result(self, sub_module_name: str,
                      start_time: datetime,
                      end_time: datetime,
                      processing_time: float,
                      local_data_file_list: Union[list, None] = None,
                      s3_data_file_list: Union[list, None] = None,
                      status: str = STATUS_SUCCESS):
        if local_data_file_list is None:
            local_data_file_list = []
        if s3_data_file_list is None:
            s3_data_file_list = []
        r = dict()
        r[self.KEY_SUB_MODULE_NAME] = sub_module_name
        r[self.KEY_DATA_FILE] = dict()
        r[self.KEY_DATA_FILE][self.KEY_DATA_FILE_LOCAL] = local_data_file_list
        r[self.KEY_DATA_FILE][self.KEY_DATA_FILE_S3] = s3_data_file_list
        r[self.KEY_STATUS] = status
        r[self.KEY_START_TIME] = start_time
        r[self.KEY_END_TIME] = end_time
        r[self.KEY_PROCESSING_TIME] = processing_time
        self._param[self.KEY_LOG].append(r)

    def get_last_log(self):
        d = self._param[self.KEY_LOG]
        if len(d) < 1:
            return None
        else:
            return self._param[self.KEY_LOG][-1]

    def get_last_value(self, key):
        last_log = self.get_last_log()
        if last_log is None:
            return None
        else:
            return last_log[key]

    def get_last_log_sub_module_name(self):
        return self.get_last_value(self.KEY_SUB_MODULE_NAME)

    def get_last_log_processing_time(self):
        return self.get_last_value(self.KEY_PROCESSING_TIME)

    def get_last_log_status(self):
        return self.get_last_value(self.KEY_STATUS)

    def get_last_log_start_time(self):
        return self.get_last_value(self.KEY_START_TIME)

    def get_last_log_end_time(self):
        return self.get_last_value(self.KEY_END_TIME)

    def get_last_log_data_file(self):
        return self.get_last_value(self.KEY_DATA_FILE)

    def get_last_log_local_data_file_list(self):
        data_file = self.get_last_value(self.KEY_DATA_FILE)
        if data_file is None:
            return None
        else:
            return data_file[self.KEY_DATA_FILE_LOCAL]

    def get_last_log_s3_data_file_list(self):
        data_file = self.get_last_value(self.KEY_DATA_FILE)
        if data_file is None:
            return None
        else:
            return data_file[self.KEY_DATA_FILE_S3]

