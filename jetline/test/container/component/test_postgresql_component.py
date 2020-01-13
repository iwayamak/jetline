# -*- coding: utf-8 -*-

import sys
from ....container.container import Container
from ....share_parameter.share_parameter import ShareParameter
from ...abc.base_test_case import BaseTestCase


class TestPostgreSQLComponent(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._component = Container.component('POSTGRESQL_COMPONENT.ID=TEST_COMPONENT')
        super().__init__(*args, **kwargs)

    def test_user(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        user = self._component.user
        self.assertEqual(user, 'test_user')

    def test_password(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        password = self._component.password
        self.assertEqual(password, 'test_password')

    def test_host(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        host = self._component.host
        self.assertEqual(host, 'test_host')

    def test_port(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        port = self._component.port
        self.assertEqual(port, 5432)

    def test_database(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        database = self._component.database
        self.assertEqual(database, 'test_database')

    def test_schema(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        schema = self._component.schema
        self.assertEqual(schema, 'test_schema')
