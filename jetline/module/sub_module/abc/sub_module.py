# -*- coding: utf-8 -*-
import time
import datetime
from abc import ABCMeta, abstractmethod
from ...sub_module.result.sub_module_result import SubModuleResult
from ....share_parameter.share_parameter import ShareParameter


class SubModule(metaclass=ABCMeta):

    def __init__(self, parameter):
        self._parameter = parameter
        self._processing_time = None
        self._result_local_file_list = None
        self._result_s3_file_list = None
        self._is_status = SubModuleResult.STATUS_ERROR
        self._start_datetime = None
        self._end_datetime = None

    def set_up(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def tear_down(self):
        ShareParameter.sub_module_result.append_result(
            self.__class__.__name__,
            self._start_datetime,
            self._end_datetime,
            self._processing_time,
            self._result_local_file_list,
            self._result_s3_file_list,
            self._is_status
        )

    def execute(self):
        self._start_datetime = datetime.datetime.now()
        try:
            self.set_up()
            self.run()
        except Exception as e:
            raise e
        else:
            self._is_status = SubModuleResult.STATUS_SUCCESS
        finally:
            self._end_datetime = datetime.datetime.now()
            self._processing_time = time.mktime(self._end_datetime.timetuple()) - time.mktime(
                self._start_datetime.timetuple())
            self.tear_down()
