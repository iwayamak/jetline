# -*- coding: utf-8 -*-

from abc import ABCMeta
from ....substr.template_yaml import TemplateYaml


class SubModuleParameter(metaclass=ABCMeta):

    def __init__(self, params=None):
        if params is not None:
            member_ls = self._value_method_name_list()
            for member_name in member_ls:
                if member_name in params:
                    v = params[member_name]
                    if isinstance(v, str):
                        t = TemplateYaml(v)
                        v = t.apply()
                    if isinstance(v, list):
                        v_temp = []
                        for elem in v:
                            if isinstance(elem, str):
                                t = TemplateYaml(elem)
                                elem = t.apply()
                            v_temp.append(elem)
                        v = v_temp
                    setattr(self, member_name, v)
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
