# -*- coding: utf-8 -*-

import copy
import logging
from .abc.component import Component

logger = logging.getLogger('jetline')


class PostgreSQLComponent(Component):

    def __init__(self, param):
        self._user = param.get('user')
        self._password = param.get('password')
        self._host = param.get('host')
        self._port = param.get('port')
        self._database = param.get('database')
        self._schema = param.get('schema')
        Component.__init__(self)

    def _validation(self):
        if self._user is None or self._password is None or \
                self._host is None or self._port is None or \
                self._database is None or self._schema is None:
            raise Exception(
                'user / password / host / port / database / schema is None!'
            )

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def database(self):
        return self._database

    @property
    def schema(self):
        return self._schema

    @classmethod
    def create_component(cls, param):
        instance = PostgreSQLComponent(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        log_dict = copy.deepcopy(instance_dict)
        log_dict['_password'] = '****'
        logger.info(f'created {cls.__name__}')
        logger.info(log_dict)
