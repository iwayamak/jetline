# -*- coding: utf-8 -*-

from jetline.exception.argument_error import ArgumentError
from ..abc.base_test_case import BaseTestCase


class TestArgumentError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(ArgumentError):
            raise ArgumentError('argument error')
