# -*- coding: utf-8 -*-

from .abc.postgresql_command import PostgreSQLCommand
from ....container.component.postgresql_component import PostgreSQLComponent


class PostgreSQLProcessingCommand(PostgreSQLCommand):

    def __init__(self, component: PostgreSQLComponent, sql_str: str):
        super().__init__(component, sql_str)

    def run(self):
        super().run()
        self._cursor.execute(self._query)
        self._connection.commit()
