# -*- coding: utf-8 -*-


class UndefinedBodyStringError(Exception):
    def __init__(self, body_str):
        info = 'undefined body string: ', body_str, ' see Template.SUB_STR!!'
        self._info = info

    def __str__(self):
        return repr(self._info)
