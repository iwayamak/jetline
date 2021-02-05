# -*- coding: utf-8 -*-

from jetline.command.db.postgresql.postgresql_processing_count_command import PostgreSQLProcessingCountCommand
from jetline.container.container import Container
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase
from jetline.exception.command_error import CommandError


class TestPostgreSQLProcessingCountCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = Container().component('POSTGRESQL_COMPONENT.ID=UT')
        self._sql_str = (
            'select count(*) from '
            '(select current_timestamp'
            ' union all'
            ' select current_timestamp union all select current_timestamp) t;'
        )
        super().__init__(*args, **kwargs)

    def test_command_dry_run(self):
        ShareParameter.dry_run_mode = True
        # assert_eq
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_eq=3
            )
        command.execute()

    def test_eq_true(self):
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_eq=3
            )
        command.execute()

    def test_eq_false(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_eq=0
                )
            command.execute()

    def test_ne_true(self):
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ne=2
            )
        command.execute()

    def test_ne_false(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ne=3
                )
            command.execute()

    def test_ge_true(self):
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=3, assert_le=3
            )
        command.execute()

    def test_ge_false(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=2, assert_le=2
                )
            command.execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_true(self):
        # assert_ge <= assert_le
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=2, assert_le=4
            )
        command.execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_false(self):
        # assert_ge <= assert_le
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4, assert_le=5
                )
            command.execute()

    def test_assert_ge_is_greater_than_assert_le_true(self):
        # assert_ge > assert_le
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
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4, assert_le=2
                )
            command.execute()

    def test_assert_ge_true(self):
        ShareParameter.dry_run_mode = False
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_ge=2
            )
        command.execute()

    def test_assert_ge_false(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_ge=4
                )
            command.execute()

    def test_assert_le_true(self):
        ShareParameter.dry_run_mode = False
        # assert_le
        command = \
            PostgreSQLProcessingCountCommand(
                self._component, self._sql_str, assert_le=4
            )
        command.execute()

    def test_assert_le_false(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str, assert_le=2
                )
            command.execute()

    def test_undefined_assert_elements(self):
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            command = \
                PostgreSQLProcessingCountCommand(
                    self._component, self._sql_str
                )
            command.execute()
