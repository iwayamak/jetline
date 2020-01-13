# -*- coding: utf-8 -*-

from .abc.sub_module_parameter import SubModuleParameter
from ...validator.validator import Validator
from ..sub_module_parameter.value.must_value import MustValue
from ..sub_module_parameter.value.option_value import OptionValue


class PluginParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._plugin_path = None
        self._package = None
        self._class_name = None
        self._kwargs = None
        super().__init__(params)

    @property
    def plugin_path(self):
        return self._plugin_path

    @plugin_path.setter
    @Validator.path
    def plugin_path(self, v):
        self._plugin_path = MustValue(v)

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, v):
        self._package = MustValue(v)

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, v):
        self._class_name = MustValue(v)

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    @Validator.dict
    def kwargs(self, v):
        self._kwargs = OptionValue(v)
