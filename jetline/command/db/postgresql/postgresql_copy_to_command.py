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


class PostgreSQLCopyToCommand(PostgreSQLCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 sql_str: str,
                 csv_file_name: str,
                 delimiter: str,
                 null_str: Union[str, None],
                 header: bool,
                 quote: str,
                 escape: str,
                 force_quote_list: Union[list, None],
                 encoding: str,
                 gzip_mode: bool):
        force_quote = None
        if force_quote_list is not None:
            force_quote = ','.join(force_quote_list)
        self._data = {
            'sql_str': sql_str.rstrip(';'),
            'csv_file_name': csv_file_name,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape,
            'force_quote': force_quote
        }
        self._csv_file_name = csv_file_name
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
        if self._gzip:
            module, mode = [gzip, 'wt']
        else:
            module, mode = [builtins, 'w']
        logger.info(f'Exporting to {self._csv_file_name}')
        with module.open(self._csv_file_name, mode=mode, encoding=self._encoding) as file:
            self._cursor.copy_expert(
                self._sql_str, file
            )
        self._connection.commit()
