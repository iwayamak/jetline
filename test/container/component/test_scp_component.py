# -*- coding: utf-8 -*-

from jetline.container.container import Container
from ...abc.base_test_case import BaseTestCase


class TestScpComponent(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container.component('SCP_COMPONENT.ID=TEST_COMPONENT')
        super().__init__(*args, **kwargs)

    def test_user(self):
        user = self._component.user
        self.assertEqual(user, 'test_user')

    def test_password(self):
        password = self._component.password
        self.assertEqual(password, 'test_password')

    def test_host(self):
        host = self._component.host
        self.assertEqual(host, 'test_host')

    def test_port(self):
        port = self._component.port
        self.assertEqual(port, 22)
