# -*- coding: utf-8 -*-

import os
import json
import logging
from jinja2 import Environment, FileSystemLoader
from .abc.confluence_command import ConfluenceCommand
from ....container.component.abc.component import Component
from ....util.file_util import FileUtil

logger = logging.getLogger('jetline')


class ConfluenceDeletePageCommand(ConfluenceCommand):

    def __init__(self,
                 component: Component,
                 page_title: str,
                 space_key: str,
                 headers: dict):
        super().__init__(component, page_title, space_key, headers)

    def set_up(self):
        super().set_up()

    def run(self):
        super().run()
        response = self._get_page_info()
        response_data = response.json()
        if response_data['size'] == 0:
            logger.info('The specified page does not exist.')
        else:
            result = response_data['results'][0]
            page_id = result['id']
            response = self._delete_page(page_id)
        response.raise_for_status()

    def _delete_page(self, page_id):
        self._url = os.path.join(self._url, page_id)
        response = self._api_delete(
            headers=self._headers
        )
        logger.info('Deleted the page')
        return response
