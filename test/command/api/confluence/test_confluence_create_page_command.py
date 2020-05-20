# -*- coding: utf-8 -*-

import os
from ....abc.base_test_case import BaseTestCase
from jetline.command.api.confluence.confluence_create_page_command import ConfluenceCreatePageCommand
from jetline.command.api.confluence.confluence_delete_page_command import ConfluenceDeletePageCommand
from jetline.container.container import Container

TEST_DATA_DIR = 'test_data'


class TestConfluenceCreatePageCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container().component('CONFLUENCE_COMPONENT.ID=UT')
        self._page_title = os.path.splitext(os.path.basename(__file__))[0]
        self._space_key = 'SPC'
        self._headers = {'content-type': 'application/json'}
        self._type = 'page'
        self._ancestors_id = '2392085'
        self._html_str = f'<div style="font-size:500%">{self._page_title}</div>'
        self._description = f'created by {os.path.basename(__file__)}'
        super().__init__(*args, **kwargs)

    def _delete_test_page(self):
        command = ConfluenceDeletePageCommand(
            self._component,
            self._page_title,
            self._space_key,
            self._headers,
        )
        command.execute()

    def _create_test_page(self):
        command = ConfluenceCreatePageCommand(
            self._component,
            self._page_title,
            self._space_key,
            self._ancestors_id,
            self._headers,
            self._html_str,
            self._description
        )
        command.execute()

    def test_create_page(self):
        self._delete_test_page()
        self._create_test_page()

    def test_update_page(self):
        self._create_test_page()
        self._create_test_page()
