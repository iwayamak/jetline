# -*- coding: utf-8 -*-

from typing import Union
from abc import ABCMeta


class SubModuleParameter(metaclass=ABCMeta):

    def __init__(self, params: Union[dict, None] = None):
        if params is not None:
            member_ls = self._value_method_name_list()
            for member_name in member_ls:
                if member_name in params:
                    value = params[member_name]
                    setattr(self, member_name, value)
                else:
                    setattr(self, member_name, None)
        else:
            member_ls = self._value_method_name_list()
            for member_name in member_ls:
                setattr(self, member_name, None)

    def _value_method_name_list(self):
        ls = []
        member_ls = dir(self)
        for member_name in member_ls:
            if member_name[0] != '_':
                ls.append(member_name)
        return ls
