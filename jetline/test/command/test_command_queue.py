# -*- coding: utf-8 -*-

import sys
from ...command.command_queue import CommandQueue
from ...container.container import Container
from ...share_parameter.share_parameter import ShareParameter
from ...command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from ..abc.base_test_case import BaseTestCase


class TestCommandQueue(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._component = Container.component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = 'select current_timestamp'
        super().__init__(*args, **kwargs)

    def test_sigle_command(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = True
        queue = CommandQueue()
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        self.assertEqual(queue._current_index, 0)
        queue.execute()
        self.assertEqual(queue._current_index, 1)

    def test_double_command(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = True
        queue = CommandQueue()
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        self.assertEqual(queue._current_index, 0)
        queue.execute()
        self.assertEqual(queue._current_index, 2)
