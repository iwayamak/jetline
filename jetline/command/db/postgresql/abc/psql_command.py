# -*- coding: utf-8 -*-

import os
import logging
from ....abc.subprocess_command import SubprocessCommand
from .....container.component.postgresql_component import PostgreSQLComponent
logger = logging.getLogger('jetline')


class PsqlCommand(SubprocessCommand):

    def __init__(self, component: PostgreSQLComponent, command_str):
        self._exec_command = None
        os.environ['PGPASSWORD'] = component.password
        psql_cmd = [
            'psql', '-p', str(component.port),
            '--host', component.host,
            '--username', component.user,
            '--dbname', component.database,
            '--command', command_str
        ]
        super().__init__(None, psql_cmd)

    def set_up(self):
        super().set_up()

    def run(self):
        super().run()
        logger.info(self._stdout.decode('utf-8').strip())

    def dry_run(self):
        super().dry_run()
