# -*- coding: utf-8 -*-

import os
import logging
from typing import Union
from jinja2 import Environment, FileSystemLoader
from ...abc.subprocess_command import SubprocessCommand
from ....container.component.postgresql_component import PostgreSQLComponent

logger = logging.getLogger('jetline')


class PostgreSQLCopyFromCommand(SubprocessCommand):

    def __init__(self,
                 component: PostgreSQLComponent,
                 table_name: str,
                 csv_file_name: str,
                 delimiter: str,
                 null_str: Union[str, None],
                 header: bool,
                 quote: str,
                 escape: str):
        self._exec_command = None
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'sql')))
        os.environ['PGPASSWORD'] = component.password
        template = env.get_template(
            os.path.splitext(os.path.basename(__file__))[0] + '.sql'
        )
        data = {
            'schema': component.schema,
            'table_name': table_name,
            'csv_file_name': csv_file_name,
            'delimiter': delimiter,
            'null_str': null_str,
            'header': header,
            'quote': quote,
            'escape': escape
        }
        rendered = template.render(data)
        psql_cmd = [
            'psql', '-p', str(component.port),
            '--host', component.host,
            '--username', component.user,
            '--dbname', component.database,
            '--command', rendered
        ]
        super().__init__(None, psql_cmd)

    def set_up(self):
        super().set_up()

    def run(self):
        super().run()
        logger.info(self._stdout.decode('utf-8').strip())

    def dry_run(self):
        super().dry_run()
        logger.info(self._exec_command)
