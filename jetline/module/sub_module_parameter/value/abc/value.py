# -*- coding: utf-8 -*-

from abc import ABCMeta


class Value(metaclass=ABCMeta):

    def __init__(self, v, display):
        self._v = v
        self._display = display

    def get(self):
        return self._v

    @property
    def display(self):
        if self._display is not None:
            return self._display
        else:
            return ''
