# -*- coding: utf-8 -*-

import sys
from .....command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from .....container.container import Container
from .....share_parameter.share_parameter import ShareParameter
from ....abc.base_test_case import BaseTestCase


class TestPostgreSQLProcessingCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._component = Container().component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = 'select current_timestamp'
        super().__init__(*args, **kwargs)

    def test_select_dry_run(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = True
        command = PostgreSQLProcessingCommand(self._component, self._sql_str)
        command.execute()

    def test_select_run(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = PostgreSQLProcessingCommand(self._component, self._sql_str)
        command.execute()
