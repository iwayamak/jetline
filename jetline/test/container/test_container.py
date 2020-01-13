# -*- coding: utf-8 -*-

import sys
from ...container.container import Container
from ..abc.base_test_case import BaseTestCase
from ...share_parameter.share_parameter import ShareParameter


class TestContainer(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def test_container(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        component = \
            Container().component(
                'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT'
            )
        self.assertEqual(component.database, 'test_database')
