# -*- coding: utf-8 -*-

import os
import gzip
import logging
import builtins
from typing import Union
from jinja2 import Environment, FileSystemLoader
from .abc.postgresql_command import PostgreSQLCommand
from ....container.component.postgresql_component import PostgreSQLComponent

logger = logging.getLogger('jetline')


class PostgreSQLCopyFromCommand(PostgreSQLCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 table_name: str,
                 column_list: Union[list, None],
                 csv_file_name_list: list,
                 delimiter: str,
                 null_str: Union[str, None],
                 header: bool,
                 quote: str,
                 escape: str,
                 encoding: str,
                 gzip_mode: bool):
        self._data = {
            'table_name': table_name,
            'column_list': column_list,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape,
        }
        self._csv_file_name_list = csv_file_name_list
        self._encoding = encoding
        self._gzip = gzip_mode
        super().__init__(component)

    def set_up(self):
        env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'sql'))
        )
        template = env.get_template(
            os.path.splitext(os.path.basename(__file__))[0] + '.sql'
        )
        self._sql_str = template.render(self._data)

    def run(self):
        super().run()
        module, mode = [gzip, 'rt'] if self._gzip else [builtins, 'r']

        for csv_file_name in self._csv_file_name_list:
            logger.info(f'Loading from {csv_file_name}')
            with module.open(csv_file_name, mode=mode, encoding=self._encoding, errors='ignore') as file:
                self._cursor.copy_expert(
                    self._sql_str,
                    file
                )
        self._connection.commit()
