# -*- coding: utf-8 -*-

from jetline.exception.command_error import CommandError
from ..abc.base_test_case import BaseTestCase


class TestCommandError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(CommandError):
            raise CommandError(1, 'command -c xxx')

    def test_raise_str(self):
        with self.assertRaises(CommandError):
            raise CommandError('error', 'command -c xxx')
