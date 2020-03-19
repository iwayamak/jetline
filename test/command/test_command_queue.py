# -*- coding: utf-8 -*-

from jetline.command.command_queue import CommandQueue
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter
from jetline.command.db.postgresql.postgresql_processing_command import PostgreSQLProcessingCommand
from ..abc.base_test_case import BaseTestCase


class TestCommandQueue(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container.component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = 'select current_timestamp'
        super().__init__(*args, **kwargs)

    def test_sigle_command(self):
        ShareParameter.dry_run_mode = True
        queue = CommandQueue()
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        self.assertEqual(queue._current_index, 0)
        queue.execute()
        self.assertEqual(queue._current_index, 1)

    def test_double_command(self):
        ShareParameter.dry_run_mode = True
        queue = CommandQueue()
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        queue.add_command(PostgreSQLProcessingCommand(self._component, self._sql_str))
        self.assertEqual(queue._current_index, 0)
        queue.execute()
        self.assertEqual(queue._current_index, 2)
