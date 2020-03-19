# -*- coding: utf-8 -*-

from ....abc.base_test_case import BaseTestCase
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter


class TestPostgreSQLProcessingCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container().component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = 'select current_timestamp'
        super().__init__(*args, **kwargs)

    def test_select_dry_run(self):
        ShareParameter.dry_run_mode = True
        command = PostgreSQLProcessingCommand(self._component, self._sql_str)
        command.execute()

    def test_select_run(self):
        ShareParameter.dry_run_mode = False
        command = PostgreSQLProcessingCommand(self._component, self._sql_str)
        command.execute()
