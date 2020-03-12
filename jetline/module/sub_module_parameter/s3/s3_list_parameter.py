# -*- coding: utf-8 -*-

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ....validator.validator import Validator


class S3ListParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._s3_component_key = None
        self._s3_file_path = None
        super().__init__(params)

    @property
    def s3_component_key(self):
        return self._s3_component_key

    @s3_component_key.setter
    @Validator.component_key
    def s3_component_key(self, v):
        self._s3_component_key = MustValue(v)

    @property
    def s3_file_path(self):
        return self._s3_file_path

    @s3_file_path.setter
    def s3_file_path(self, v):
        self._s3_file_path = MustValue(v)
