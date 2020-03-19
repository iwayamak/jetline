# -*- coding: utf-8 -*-

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from ..abc.base_test_case import BaseTestCase


class TestSubModuleParameterError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(SubModuleParameterError):
            raise SubModuleParameterError('validator_name', 'target')
