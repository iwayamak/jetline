# -*- coding: utf-8 -*-

from jetline.exception.template_string.sub_string_error import TemplateStringError
from ...abc.base_test_case import BaseTestCase


class TestTemplateStringError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(TemplateStringError):
            raise TemplateStringError('template string error')
