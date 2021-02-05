# -*- coding: utf-8 -*-

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ..value.option_value import OptionValue
from ....validator.validator import Validator


class ScpGetParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._scp_component_key = None
        self._remote_path = None
        self._local_dir_path = None
        self._recursive = None
        self._preserve_times = None
        super().__init__(params)

    @property
    def scp_component_key(self):
        return self._scp_component_key

    @scp_component_key.setter
    @Validator.component_key
    def scp_component_key(self, v):
        self._scp_component_key = MustValue(v)

    @property
    def remote_path(self):
        return self._remote_path

    @remote_path.setter
    def remote_path(self, v):
        self._remote_path = MustValue(v)

    @property
    def local_dir_path(self):
        return self._local_dir_path

    @local_dir_path.setter
    def local_dir_path(self, v):
        self._local_dir_path = MustValue(v)

    @property
    def recursive(self):
        return self._recursive

    @recursive.setter
    @Validator.boolean
    def recursive(self, v):
        self._recursive = OptionValue(v, default=False)

    @property
    def preserve_times(self):
        return self._preserve_times

    @preserve_times.setter
    @Validator.boolean
    def preserve_times(self, v):
        self._preserve_times = OptionValue(v, default=False)
