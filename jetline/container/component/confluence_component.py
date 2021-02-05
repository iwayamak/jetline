# -*- coding: utf-8 -*-

import copy
import logging
from .abc.component import Component

logger = logging.getLogger('jetline')


class ConfluenceComponent(Component):

    def __init__(self, param):
        self._url = param.get('url')
        self._user = param.get('user')
        self._password = param.get('password')
        Component.__init__(self)

    def _validation(self):
        if self._url is None or self._user is None or self._password is None:
            raise Exception(
                'url / user / password is None!'
            )

    @property
    def url(self):
        return self._url

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @classmethod
    def create_component(cls, param):
        instance = ConfluenceComponent(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        log_dict = copy.deepcopy(instance_dict)
        log_dict["_password"] = '****'
        logger.info(f'created {cls.__name__}')
        logger.info(log_dict)
