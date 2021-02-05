# -*- coding: utf-8 -*-


class BodyStringError(Exception):

    def __init__(self, body_str):
        info = 'invalid body str: ', body_str, \
               ' body str is inner string of template string. like this ${<body string>}.'
        self._info = info

    def __str__(self):
        return repr(self._info)
