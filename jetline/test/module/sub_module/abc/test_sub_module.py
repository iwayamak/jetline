# -*- coding: utf-8 -*-

import sys
from .....module.sub_module.abc.sub_module import SubModule
from .....module.sub_module_parameter.abc.sub_module_parameter import SubModuleParameter
from .....module.sub_module.result.sub_module_result import SubModuleResult
from .....module.sub_module_parameter.value.option_value import OptionValue
from .....share_parameter.share_parameter import ShareParameter
from ....abc.base_test_case import BaseTestCase


class ChileSubModuleParameter(SubModuleParameter):

    def __init__(self, params):
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
        self._class_name = self.__class__.__name__
        super(TestSubModule, self).__init__(*args, **kwargs)

    def setUp(self):
        ShareParameter.sub_module_result = SubModuleResult()

    def test_simple(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        param_dict = {'member_a': '1', 'member_b': '2'}
        parameter = ChileSubModuleParameter(param_dict)
        sub_module = ChildSubModule(parameter)
        self.assertEqual('1', sub_module._parameter.member_a)
        self.assertEqual('2', sub_module._parameter.member_b)
        sub_module.execute()

    def test_none_param(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        parameter = ChileSubModuleParameter(None)
        self.assertEqual(None, parameter.member_b)
