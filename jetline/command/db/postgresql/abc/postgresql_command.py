# -*- coding: utf-8 -*-

import psycopg2
from typing import Union
from ...abc.db_command import DbCommand
from .....container.component.postgresql_component import PostgreSQLComponent


class PostgreSQLCommand(DbCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 sql_str: Union[str, None] = None):
        self._sql_str = sql_str
        super().__init__(component)

    def run(self):
        self._connection = \
            psycopg2.connect(
                database=self.component.database,
                user=self.component.user,
                password=self.component.password,
                host=self.component.host,
                port=self.component.port
            )
        self._connection.set_client_encoding('utf-8')
        super().run()

    def _query_builder(self):
        return self._sql_str

    def _mask_password(self):
        return self._sql_str
