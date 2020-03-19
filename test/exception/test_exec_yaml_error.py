# -*- coding: utf-8 -*-

from jetline.exception.exec_yaml_error import ExecYamlError
from ..abc.base_test_case import BaseTestCase


class TestExecYamlError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(ExecYamlError):
            raise ExecYamlError('exec yaml error')
