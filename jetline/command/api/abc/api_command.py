# -*- coding: utf-8 -*-

import logging
import requests
from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class ApiCommand(Command):

    def __init__(self, component: Component, timeout=1800):
        self._session = requests.Session()
        self._response = None
        self._timeout = timeout
        self._url = None
        super().__init__(component)

    def set_up(self):
        logger.info(f'headers: {self._session.headers}')

        self._url = self.component.url
        logger.info(f'url: {self._url}')

        super().set_up()

    def body(self):
        super().body()

    def run(self):
        super().run()

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        if self._session is not None:
            self._session.close()
        if self._response is not None:
            self._response.close()
        super().tear_down()

    def _api_get(self, **kwargs):
        response = self._session.get(
            self._url,
            **kwargs
        )
        return response

    def _api_post(self, **kwargs):
        response = self._session.post(
            self._url,
            **kwargs
        )
        return response

    def _api_put(self, **kwargs):
        response = self._session.put(
            self._url,
            **kwargs
        )
        return response

    def _api_delete(self, **kwargs):
        response = self._session.delete(
            self._url,
            **kwargs
        )
        return response
