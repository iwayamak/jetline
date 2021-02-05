# -*- coding: utf-8 -*-

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.option_value import OptionValue
from ....validator.validator import Validator


class LocalProcessingRemoveParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._path_list = None
        self._use_last_result = None
        super().__init__(params)

    @property
    def path_list(self):
        return self._path_list

    @path_list.setter
    @Validator.list
    def path_list(self, v):
        self._path_list = OptionValue(v)

    @property
    def use_last_result(self):
        return self._use_last_result

    @use_last_result.setter
    @Validator.boolean
    def use_last_result(self, v):
        self._use_last_result = OptionValue(v, default=False)
