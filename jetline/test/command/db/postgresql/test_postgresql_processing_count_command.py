# -*- coding: utf-8 -*-

import sys
from .....command.db.postgresql.postgresql_processing_count_command import PostgreSQLProcessingCountCommand
from .....container.container import Container
from .....share_parameter.share_parameter import ShareParameter
from .....test.abc.base_test_case import BaseTestCase
from .....exception.command_error import CommandError


class TestPostgreSQLProcessingCountCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._class_name = self.__class__.__name__
        self._component = Container().component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = (
            'select count(*) from '
            '(select current_timestamp'
            ' union all'
            ' select current_timestamp union all select current_timestamp) t;'
        )
        super().__init__(*args, **kwargs)

    def test_command_dry_run(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = True
        # assert_eq
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_eq=3
            )
        command.execute()

    def test_eq_true(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_eq=3
            )
        command.execute()

    def test_eq_false(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_eq=0
                )
            command.execute()

    def test_ne_true(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ne=2
            )
        command.execute()

    def test_ne_false(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ne=3
                )
            command.execute()

    def test_ge_true(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=3, assert_le=3
            )
        command.execute()

    def test_ge_false(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=2, assert_le=2
                )
            command.execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_true(self):
        # assert_ge <= assert_le
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=2, assert_le=4
            )
        command.execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_false(self):
        # assert_ge <= assert_le
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4, assert_le=5
                )
            command.execute()

    def test_assert_ge_is_greater_than_assert_le_true(self):
        # assert_ge > assert_le
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=3, assert_le=2
            )
        command.execute()

        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=4, assert_le=3
            )
        command.execute()

    def test_assert_ge_is_greater_than_assert_le_false(self):
        # assert_ge > assert_le
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4, assert_le=2
                )
            command.execute()

    def test_assert_ge_true(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=2
            )
        command.execute()

    def test_assert_ge_false(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4
                )
            command.execute()

    def test_assert_le_true(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        # assert_le
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_le=4
            )
        command.execute()

    def test_assert_le_false(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_le=2
                )
            command.execute()

    def test_undefined_assert_elements(self):
        method_name = sys._getframe().f_code.co_name
        ShareParameter.batch_name = self._class_name + '_' + method_name
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str
                )
            command.execute()
