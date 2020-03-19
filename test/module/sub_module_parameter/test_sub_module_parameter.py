# -*- coding: utf-8 -*-

from test.abc.base_test_case import BaseTestCase
from jetline.module.sub_module_parameter.abc.sub_module_parameter import SubModuleParameter
from jetline.module.sub_module_parameter.value.must_value import MustValue
from jetline.module.sub_module_parameter.value.option_value import OptionValue
from jetline.exception.sub_module_parameter_error import SubModuleParameterError


MEMBER_A = 'member_a is member_a'
MEMBER_B = 'member_b is member_b'


class ASubModuleParameter(SubModuleParameter):

    def __init__(self, params: dict):
        self._member_a = None
        self._member_b = None
        super().__init__(params)

    @property
    def member_a(self):
        return self._member_a

    @member_a.setter
    def member_a(self, v):
        self._member_a = MustValue(v, display=MEMBER_A)

    @property
    def member_b(self):
        return self._member_b

    @member_b.setter
    def member_b(self, v):
        self._member_b = OptionValue(v, display=MEMBER_B)


class TestSubModuleParameter(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestSubModuleParameter, self).__init__(*args, **kwargs)

    def test_all_parameter(self):
        params = {'member_a': '1', 'member_b': '2'}
        o = ASubModuleParameter(params)
        self.assertEqual('1', o.member_a.get())
        self.assertEqual('2', o.member_b.get())
        self.assertEqual(MEMBER_A, o.member_a.display)
        self.assertEqual(MEMBER_B, o.member_b.display)

    def test_must_parameter_not_set(self):
        params = {'member_b': '2'}
        with self.assertRaises(SubModuleParameterError):
            ASubModuleParameter(params)

    def test_must_parameter(self):
        params = {'member_a': '1'}
        o = ASubModuleParameter(params)
        self.assertEqual('1', o.member_a.get())
        self.assertIsNone(o.member_b.get())
        self.assertEqual(MEMBER_A, o.member_a.display)
        self.assertEqual(MEMBER_B, o.member_b.display)

    def test_mix_in_parameter(self):
        params = {
            'member_a': '1',
            'member_b': '2',
            'member_c': {
                'member_c_1': 'c_1', 'member_c_2': 'c_2'
            }
        }
        o = ASubModuleParameter(params)
        self.assertEqual('1', o.member_a.get())
        self.assertEqual('2', o.member_b.get())
        with self.assertRaises(AttributeError):
            o._member_c
