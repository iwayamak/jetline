# -*- coding: utf-8 -*-

import os
import json
import logging
from jinja2 import Environment, FileSystemLoader
from .abc.confluence_command import ConfluenceCommand
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class ConfluenceCreatePageCommand(ConfluenceCommand):

    def __init__(self,
                 component: Component,
                 page_title: str,
                 space_key: str,
                 ancestors_id: str,
                 headers: dict,
                 html_str: str,
                 description: str):
        self._data = {
            'description': description,
            'table': html_str
        }
        self._ancestors_id = ancestors_id
        self._json_data = None
        super().__init__(component, page_title, space_key, headers)

    def set_up(self):
        super().set_up()
        env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html'))
        )
        template = env.get_template(
            os.path.splitext(os.path.basename(__file__))[0] + '.html'
        )
        self._html = template.render(self._data)

    def run(self):
        super().run()
        self._json_data = self._create_json_data()
        response = self._get_page_info()
        response_data = response.json()
        if response_data['size'] == 0:
            response = self._create_page()
        else:
            result = response_data['results'][0]
            new_version_number = result['version']['number'] + 1
            page_id = result['id']
            response = self._update_page(new_version_number, page_id)
        response.raise_for_status()

    def _create_json_data(self):
        json_dict = {
            'type': 'page',
            'title': self._page_title,
            'ancestors': [{'id': self._ancestors_id}],
            'space': {'key': self._space_key},
            'body': {
                'storage': {
                    'value': self._html,
                    'representation': 'storage'
                }
            }
        }
        return json_dict

    def _create_page(self):
        response = self._api_post(
            data=json.dumps(self._json_data),
            headers=self._headers
        )
        logger.info('Created the page')
        return response

    def _update_page(self, new_version_number, page_id):
        self._json_data['version'] = {'number': new_version_number}
        self._url = os.path.join(self._url, page_id)
        response = self._api_put(
            data=json.dumps(self._json_data),
            headers=self._headers
        )
        logger.info('Updated the page')
        logger.info(f'new_version_number: {new_version_number}')
        logger.info(f'page_id: {page_id}')
        return response
