# -*- coding: utf-8 -*-


class SubModuleParameterError(Exception):

    def __init__(self, validator_name, target):
        self._info = \
            f'sub_module_parameter is invalid. validator: {validator_name} target: {target}'

    def __str__(self):
        return repr(self._info)
