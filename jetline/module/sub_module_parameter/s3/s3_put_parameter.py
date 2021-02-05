# -*- coding: utf-8 -*-

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ..value.option_value import OptionValue
from ....validator.validator import Validator


class S3PutParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._s3_component_key = None
        self._local_file_path = None
        self._s3_dir_path = None
        self._end_file_name = None
        super().__init__(params)

    @property
    def s3_component_key(self):
        return self._s3_component_key

    @s3_component_key.setter
    @Validator.component_key
    def s3_component_key(self, v):
        self._s3_component_key = MustValue(v)

    @property
    def local_file_path(self):
        return self._local_file_path

    @local_file_path.setter
    def local_file_path(self, v):
        self._local_file_path = OptionValue(v)

    @property
    def s3_dir_path(self):
        return self._s3_dir_path

    @s3_dir_path.setter
    def s3_dir_path(self, v):
        self._s3_dir_path = MustValue(v)

    @property
    def end_file_name(self):
        return self._end_file_name

    @end_file_name.setter
    def end_file_name(self, v):
        self._end_file_name = OptionValue(v, default=None)
