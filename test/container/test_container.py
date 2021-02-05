# -*- coding: utf-8 -*-

from jetline.container.container import Container
from ..abc.base_test_case import BaseTestCase


class TestContainer(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_container(self):
        component = \
            Container().component(
                'POSTGRESQL_COMPONENT.ID=TEST_COMPONENT'
            )
        self.assertEqual(component.database, 'test_database')
