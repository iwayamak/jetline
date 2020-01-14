# -*- coding: utf-8 -*-

from .abc.value import Value
from ....exception.sub_module_parameter_error import SubModuleParameterError


class MustValue(Value):

    def __init__(self, v, display=None):
        if v is None:
            raise SubModuleParameterError("MustValue", "None")
        super(MustValue, self).__init__(v, display)
