# -*- coding: utf-8 -*-

from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue
from .....validator.validator import Validator


class PostgreSQLProcessingParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._postgresql_component_key = None
        self._sql_file_name = None
        self._input_value = None
        super().__init__(params)

    @property
    def postgresql_component_key(self):
        return self._postgresql_component_key

    @postgresql_component_key.setter
    @Validator.component_key
    def postgresql_component_key(self, v):
        self._postgresql_component_key = MustValue(v)

    @property
    def sql_file_name(self):
        return self._sql_file_name

    @sql_file_name.setter
    @Validator.path
    def sql_file_name(self, v):
        self._sql_file_name = MustValue(v)

    @property
    def input_value(self):
        return self._input_value

    @input_value.setter
    @Validator.dict
    def input_value(self, v):
        self._input_value = OptionValue(v)

