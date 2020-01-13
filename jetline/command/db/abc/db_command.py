# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta, abstractmethod
from ....command.abc.command import Command
from ....substr.template import Template

logger = logging.getLogger('jetline')


class DbCommand(Command, metaclass=ABCMeta):

    def __init__(self, component):
        self._query = None
        self._cursor = None
        self._connection = None
        super().__init__(component)

    def set_up(self):
        super().set_up()

    def body(self):
        self._query = self._query_builder()
        super().body()

    def run(self):
        super().run()
        self._cursor = self._connection.cursor()
        logger.info('Performing queries\n{0}'.format(self._mask_password()))
        self._cursor.execute(self._query)
        self._connection.commit()

    def dry_run(self):
        super().dry_run()
        logger.info('Dry run queries\n{0}'.format(self._mask_password()))

    def tear_down(self):
        if self._cursor is not None:
            self._cursor.close()
        super().tear_down()

    @abstractmethod
    def _query_builder(self):
        pass

    @abstractmethod
    def _mask_password(self):
        pass

    @classmethod
    def create_query(cls, sql_str):
        if sql_str is not None:
            template = Template(sql_str)
            q = template.apply()
        else:
            q = None
        return q
