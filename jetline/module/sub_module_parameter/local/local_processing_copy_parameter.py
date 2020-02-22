# -*- coding: utf-8 -*-

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue


class LocalProcessingCopyParameter(SubModuleParameter):

    def __init__(self, params=None):
        self._source_path = None
        self._destination_path = None
        super().__init__(params)

    @property
    def source_path(self):
        return self._source_path

    @source_path.setter
    def source_path(self, v):
        self._source_path = MustValue(v)

    @property
    def destination_path(self):
        return self._destination_path

    @destination_path.setter
    def destination_path(self, v):
        self._destination_path = MustValue(v)
