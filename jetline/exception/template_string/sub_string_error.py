# -*- coding: utf-8 -*-


class TemplateStringError(Exception):

    def __init__(self, info):
        self._info = info

    def __str__(self):
        return repr(self._info)
