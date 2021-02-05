# -*- coding: utf-8 -*-

import os
from ....abc.base_test_case import BaseTestCase
from jetline.command.api.confluence.confluence_create_page_command import ConfluenceCreatePageCommand
from jetline.command.api.confluence.confluence_delete_page_command import ConfluenceDeletePageCommand
from jetline.container.container import Container

TEST_DATA_DIR = 'test_data'


class TestConfluenceDeletePageCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container().component('CONFLUENCE_COMPONENT.ID=UT')
        self._page_title = os.path.splitext(os.path.basename(__file__))[0]
        self._space_key = 'SPC'
        self._headers = {'content-type': 'application/json'}
        self._type = 'page'
        self._ancestors_id = '2392085'
        self._description = f'created by {os.path.basename(__file__)}'
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), TEST_DATA_DIR
            )
        super().__init__(*args, **kwargs)

    def _create_test_page(self):
        command = ConfluenceCreatePageCommand(
            self._component,
            self._page_title,
            self._space_key,
            self._ancestors_id,
            self._headers,
            os.path.join(
                self._test_data_path,
                'test_confluence_command.json'
            ),
            self._description
        )
        command.execute()

    def test_delete_page(self):
        self._create_test_page()
        command = ConfluenceDeletePageCommand(
            self._component,
            self._page_title,
            self._space_key,
            self._headers,
        )
        command.execute()

    def test_delete_page_not_exists(self):
        command = ConfluenceDeletePageCommand(
            self._component,
            'page_not_exists',
            self._space_key,
            self._headers,
        )
        command.execute()
