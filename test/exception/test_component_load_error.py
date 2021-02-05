# -*- coding: utf-8 -*-

from jetline.exception.component_load_error import ComponentLoadError
from ..abc.base_test_case import BaseTestCase


class TestComponentLoadError(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_raise(self):
        with self.assertRaises(ComponentLoadError):
            raise ComponentLoadError("test_component")
