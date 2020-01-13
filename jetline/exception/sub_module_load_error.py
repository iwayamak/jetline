# -*- coding: utf-8 -*-


class SubModuleLoadError(Exception):

    def __init__(self, sub_module_name):
        info = 'Fail sub module load: {0}'
        self._info = info.format(sub_module_name)

    def __str__(self):
        return repr(self._info)
