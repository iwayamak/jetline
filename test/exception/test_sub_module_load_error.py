# -*- coding: utf-8 -*-

from jetline.exception.sub_module_load_error import SubModuleLoadError
from ..abc.base_test_case import BaseTestCase


class TestSubModuleLoadError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(SubModuleLoadError):
            raise SubModuleLoadError('test_sub_module')
