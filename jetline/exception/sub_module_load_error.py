# -*- coding: utf-8 -*-


class SubModuleLoadError(Exception):

    def __init__(self, sub_module_name):
        self._info = f'Fail sub module load: {sub_module_name}'

    def __str__(self):
        return repr(self._info)
