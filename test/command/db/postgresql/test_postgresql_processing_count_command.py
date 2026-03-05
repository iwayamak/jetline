"""PostgreSQLProcessingCountCommand のユニットテスト."""

from jetline.command.db.postgresql.postgresql_processing_count_command import (
    PostgreSQLProcessingCountCommand,
)
from jetline.container.container import Container
from jetline.exception.command_error import CommandError
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase


class TestPostgreSQLProcessingCountCommand(BaseTestCase):
    """集計件数アサートの各条件分岐を検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._component = Container().component("POSTGRESQL_COMPONENT.ID=UT")
        self._sql_str = (
            "select count(*) from "
            "(select current_timestamp"
            " union all"
            " select current_timestamp union all select current_timestamp) t;"
        )
        super().__init__(*args, **kwargs)

    def _new_command(self, **conditions: int) -> PostgreSQLProcessingCountCommand:
        """件数アサート付きコマンドを生成する.

        Args:
            **conditions: `assert_eq` などの条件値.

        Returns:
            PostgreSQLProcessingCountCommand: 生成したコマンド.
        """
        return PostgreSQLProcessingCountCommand(self._component, self._sql_str, **conditions)

    def test_command_dry_run(self) -> None:
        """Dry-run で件数アサート付きコマンドが実行できることを確認する."""
        ShareParameter.dry_run_mode = True
        self._new_command(assert_eq=3).execute()

    def test_eq_true(self) -> None:
        """`assert_eq` が成立する場合に成功することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_eq=3).execute()

    def test_eq_false(self) -> None:
        """`assert_eq` が不成立の場合に例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_eq=0).execute()

    def test_ne_true(self) -> None:
        """`assert_ne` が成立する場合に成功することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_ne=2).execute()

    def test_ne_false(self) -> None:
        """`assert_ne` が不成立の場合に例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_ne=3).execute()

    def test_ge_true(self) -> None:
        """`assert_ge` / `assert_le` の両方が成立することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_ge=3, assert_le=3).execute()

    def test_ge_false(self) -> None:
        """範囲外の場合に例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_ge=2, assert_le=2).execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_true(self) -> None:
        """`assert_ge <= assert_le` で範囲内なら成功することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_ge=2, assert_le=4).execute()

    def test_assert_ge_is_less_than_or_equal_to_assert_le_false(self) -> None:
        """`assert_ge <= assert_le` で範囲外なら失敗することを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_ge=4, assert_le=5).execute()

    def test_assert_ge_is_greater_than_assert_le_true(self) -> None:
        """`assert_ge > assert_le` の OR 条件成立ケースを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_ge=3, assert_le=2).execute()
        self._new_command(assert_ge=4, assert_le=3).execute()

    def test_assert_ge_is_greater_than_assert_le_false(self) -> None:
        """`assert_ge > assert_le` の OR 条件不成立ケースを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_ge=4, assert_le=2).execute()

    def test_assert_ge_true(self) -> None:
        """`assert_ge` 単独条件が成立することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_ge=2).execute()

    def test_assert_ge_false(self) -> None:
        """`assert_ge` 単独条件が不成立で例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_ge=4).execute()

    def test_assert_le_true(self) -> None:
        """`assert_le` 単独条件が成立することを確認する."""
        ShareParameter.dry_run_mode = False
        self._new_command(assert_le=4).execute()

    def test_assert_le_false(self) -> None:
        """`assert_le` 単独条件が不成立で例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command(assert_le=2).execute()

    def test_undefined_assert_elements(self) -> None:
        """アサート条件未指定時に例外となることを確認する."""
        ShareParameter.dry_run_mode = False
        with self.assertRaises(CommandError):
            self._new_command().execute()
