# -*- coding: utf-8 -*-


class SubModuleParameterError(Exception):

    def __init__(self, validator_name, target):
        info = 'sub_module_parameter is invalid. validator: {0} target: {1}'
        self._info = info.format(validator_name, target)

    def __str__(self):
        return repr(self._info)
