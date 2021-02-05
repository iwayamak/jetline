# -*- coding: utf-8 -*-

from jetline.exception.template_string.body_string_error import BodyStringError
from ...abc.base_test_case import BaseTestCase


class TestBodyStringError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(BodyStringError):
            raise BodyStringError('body string error')
