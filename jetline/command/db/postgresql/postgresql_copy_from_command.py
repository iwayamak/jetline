# -*- coding: utf-8 -*-

import os
from typing import Union
from jinja2 import Environment, FileSystemLoader
from .abc.postgresql_command import PostgreSQLCommand
from ....container.component.postgresql_component import PostgreSQLComponent


class PostgreSQLCopyFromCommand(PostgreSQLCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 table_name: str,
                 csv_file_name: str,
                 delimiter: str,
                 null_str: Union[str, None],
                 header: bool,
                 quote: str,
                 escape: str):
        self._data = {
            'schema': component.schema,
            'table_name': table_name,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape
        }
        self._csv_file_name = csv_file_name
        super().__init__(component)

    def set_up(self):
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'sql')))
        template = env.get_template(
            os.path.splitext(os.path.basename(__file__))[0] + '.sql'
        )
        self._sql_str = template.render(self._data)

    def run(self):
        super().run()
        with open(self._csv_file_name, mode='r', encoding='utf8') as file:
            self._cursor.copy_expert(
                self._sql_str,
                file
            )
        self._connection.commit()
