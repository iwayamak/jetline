# -*- coding: utf-8 -*-

from jetline.exception.template_string.undefined_body_string_error import UndefinedBodyStringError
from ...abc.base_test_case import BaseTestCase


class TestUndefinedBodyStringError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(UndefinedBodyStringError):
            raise UndefinedBodyStringError('undefined body string error')
