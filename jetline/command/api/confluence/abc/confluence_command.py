# -*- coding: utf-8 -*-

from ...abc.api_command import ApiCommand
from .....container.component.abc.component import Component


class ConfluenceCommand(ApiCommand):

    def __init__(self, component: Component,  page_title: str, space_key: str, headers: dict):
        self._page_title = page_title
        self._space_key = space_key
        self._headers = headers
        self._html = None
        super().__init__(component)

    def run(self):
        super().run()
        self._session.auth = (self.component.user, self.component.password)

    def dry_run(self):
        super().dry_run()

    def _get_page_info(self):
        response = self._api_get(
            params={
                'title': self._page_title,
                'spaceKey': self._space_key,
                'expand': 'version,history'
            },
            headers=self._headers
        )
        return response
