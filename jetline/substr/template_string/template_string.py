# -*- coding: utf-8 -*-

from abc import ABCMeta


class TemplateString(metaclass=ABCMeta):

    def __init__(self):
        self._result = None
        self._str_format = None
        self._query_mode = True
        self._option = None

    @property
    def str_format(self):
        return self._str_format

    @str_format.setter
    def str_format(self, value):
        self._str_format = value

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, value):
        self._option = value

    @property
    def query_mode(self):
        return self._query_mode

    @query_mode.setter
    def query_mode(self, value):
        self._query_mode = value

    @property
    def result(self):
        if self._result is None:
            self.evaluate()
        return self._result

    @result.deleter
    def result(self):
        self._result = None

    def evaluate(self):
        self._escape()

    def _validate(self):
        pass

    def _escape(self):
        if self._query_mode:
            if self._result.isdigit():
                pass
            else:
                self._result = '\'' + self._result + '\''
