# -*- coding: utf-8 -*-

import sys
from ....share_parameter.share_parameter import ShareParameter
from ....exception.template_string.undefined_body_string_error import UndefinedBodyStringError
from ...abc.base_test_case import BaseTestCase


class TestUndefinedBodyStringError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def test_raise(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        with self.assertRaises(UndefinedBodyStringError):
            raise UndefinedBodyStringError('undefined body string error')
