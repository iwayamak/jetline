# -*- coding: utf-8 -*-

from typing import Union
from jetline.module.sub_module.abc.sub_module import SubModule
from jetline.module.sub_module_parameter.abc.sub_module_parameter import SubModuleParameter
from jetline.module.sub_module.result.sub_module_result import SubModuleResult
from jetline.module.sub_module_parameter.value.option_value import OptionValue
from jetline.share_parameter.share_parameter import ShareParameter
from ....abc.base_test_case import BaseTestCase


class ChileSubModuleParameter(SubModuleParameter):

    def __init__(self, params: Union[dict, None]):
        self._member_a = None
        self._member_b = None
        super(ChileSubModuleParameter, self).__init__(params)

    @property
    def member_a(self):
        return self._member_a.get()

    @property
    def member_b(self):
        return self._member_b.get()

    @member_a.setter
    def member_a(self, v):
        self._member_a = OptionValue(v)

    @member_b.setter
    def member_b(self, v):
        self._member_b = OptionValue(v)


class ChildSubModule(SubModule):
    def __init__(self, param):
        super(ChildSubModule, self).__init__(param)

    def run(self):
        pass


class TestSubModule(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestSubModule, self).__init__(*args, **kwargs)

    def setUp(self):
        ShareParameter.sub_module_result = SubModuleResult()

    def test_simple(self):
        param_dict = {'member_a': '1', 'member_b': '2'}
        parameter = ChileSubModuleParameter(param_dict)
        sub_module = ChildSubModule(parameter)
        self.assertEqual('1', sub_module._parameter.member_a)
        self.assertEqual('2', sub_module._parameter.member_b)
        sub_module.execute()

    def test_none_param(self):
        parameter = ChileSubModuleParameter(None)
        self.assertEqual(None, parameter.member_b)
