# -*- coding: utf-8 -*-


class ComponentLoadError(Exception):

    def __init__(self, component_name):
        info = 'Fail component load: {0}'
        self._info = info.format(component_name)

    def __str__(self):
        return repr(self._info)
