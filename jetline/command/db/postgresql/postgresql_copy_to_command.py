# -*- coding: utf-8 -*-

import os
import logging
from typing import Union
from jinja2 import Environment, FileSystemLoader
from .abc.psql_command import PsqlCommand
from ....container.component.postgresql_component import PostgreSQLComponent

logger = logging.getLogger('jetline')


class PostgreSQLCopyToCommand(PsqlCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 sql_str: str,
                 csv_file_name: str,
                 delimiter: str,
                 null_str: Union[str, None],
                 header: bool,
                 quote: str,
                 escape: str,
                 force_quote_list: Union[list, None]):
        self._exec_command = None
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'sql')))
        template = env.get_template(
            os.path.splitext(os.path.basename(__file__))[0] + '.sql'
        )
        force_quote = None
        if force_quote_list is not None:
            force_quote = ','.join(force_quote_list)
        data = {
            'sql_str': sql_str.rstrip(';'),
            'csv_file_name': csv_file_name,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape,
            'force_quote': force_quote
        }
        command_str = template.render(data)
        super().__init__(component, command_str)

    def set_up(self):
        super().set_up()

    def dry_run(self):
        super().dry_run()
        logger.info(self._exec_command)
