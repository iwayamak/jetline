# -*- coding: utf-8 -*-

from jetline.container.container import Container
from ...abc.base_test_case import BaseTestCase


class TestPluginComponent(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container.component('PLUGIN_COMPONENT.ID=TEST_COMPONENT')
        super().__init__(*args, **kwargs)

    def test_param1(self):
        param = self._component.param1
        self.assertEqual(param, 'Param_01')

    def test_param2(self):
        param = self._component.param2
        self.assertEqual(param, 'Param_02')
