# -*- coding: utf-8 -*-

from .abc.value import Value


class OptionValue(Value):

    def __init__(self, v, default=None, display=None):
        if v is None:
            v = default
        super(OptionValue, self).__init__(v, display)
