"""PostgreSQL 件数検証付き SQL 実行コマンド."""

import logging

from ....container.component.postgresql_component import PostgreSQLComponent
from ....exception.command_error import CommandError
from .abc.postgresql_command import PostgreSQLCommand

logger = logging.getLogger("jetline")


class PostgreSQLProcessingCountCommand(PostgreSQLCommand):
    """件数検証条件に基づいて SQL 実行結果を評価する."""

    def __init__(
        self,
        component: PostgreSQLComponent,
        sql_str: str,
        assert_eq: int | None = None,
        assert_ne: int | None = None,
        assert_ge: int | None = None,
        assert_le: int | None = None,
    ):
        """件数検証コマンドを初期化する.

        Args:
            component: PostgreSQL コンポーネント.
            sql_str: 実行対象 SQL（1 行 1 列で件数を返す想定）.
            assert_eq: 件数が一致すべき値.
            assert_ne: 件数が不一致であるべき値.
            assert_ge: 件数の下限.
            assert_le: 件数の上限.
        """
        self._assert_eq = assert_eq
        self._assert_ne = assert_ne
        self._assert_ge = assert_ge
        self._assert_le = assert_le
        super().__init__(component, sql_str)

    def run(self):
        """SQL 実行結果の件数を検証する."""
        super().run()
        count = self._fetch_count()
        logger.info("count: %s", count)
        self._validate_count(count)

    def _fetch_count(self) -> int:
        """SQL 実行結果から件数値を取得する.

        Returns:
            int: 取得した件数.

        Raises:
            CommandError: 1行1列で件数が取得できない場合.
        """
        self.execute_query(commit=True)
        row = self._cursor.fetchone()
        if row is None:
            raise CommandError(
                return_code="row_count: 0",
                cmd=self._mask_password(),
            )
        if len(row) != 1:
            raise CommandError(
                return_code=f"column_count: {len(row)}",
                cmd=self._mask_password(),
            )
        extra_row = self._cursor.fetchone()
        if extra_row is not None:
            raise CommandError(
                return_code="row_count: 2 or more",
                cmd=self._mask_password(),
            )

        count = row[0]
        if not isinstance(count, int):
            raise CommandError(
                return_code=f"count: {count}",
                cmd=self._mask_password(),
            )
        return count

    def _validate_count(self, count: int) -> None:
        """件数をアサーション条件と照合する.

        Args:
            count: 検証対象の件数.

        Raises:
            CommandError: 条件を満たさない場合.
        """
        if self._assert_eq is not None:
            self._validate_equal(count)
            return
        if self._assert_ne is not None:
            self._validate_not_equal(count)
            return
        if self._assert_ge is not None and self._assert_le is not None:
            self._validate_range(count)
            return
        if self._assert_ge is not None:
            self._validate_greater_equal(count)
            return
        if self._assert_le is not None:
            self._validate_less_equal(count)
            return
        raise self._new_assertion_error("Undefined assert_eq, assert_ne, assert_ge, assert_le.")

    def _validate_equal(self, count: int) -> None:
        """等価条件を検証する."""
        message = f"count: {count} == assert_eq: {self._assert_eq}"
        logger.debug(message)
        if count != self._assert_eq:
            raise self._new_assertion_error(message)

    def _validate_not_equal(self, count: int) -> None:
        """非等価条件を検証する."""
        message = f"count: {count} != assert_ne: {self._assert_ne}"
        logger.debug(message)
        if count == self._assert_ne:
            raise self._new_assertion_error(message)

    def _validate_range(self, count: int) -> None:
        """上下限条件を検証する."""
        assert_ge = self._assert_ge
        assert_le = self._assert_le
        if assert_ge is None or assert_le is None:
            raise self._new_assertion_error("Undefined assert_ge or assert_le.")

        if assert_ge <= assert_le:
            message = f"assert_ge: {assert_ge} <= count: {count} <= assert_le: {assert_le}"
            logger.debug(message)
            if not (assert_ge <= count <= assert_le):
                raise self._new_assertion_error(message)
            return

        message = (
            f"count: {count} <= assert_le: {assert_le} "
            f"or assert_ge: {assert_ge} <= count: {count}"
        )
        logger.debug(message)
        if not (count <= assert_le or assert_ge <= count):
            raise self._new_assertion_error(message)

    def _validate_greater_equal(self, count: int) -> None:
        """下限条件を検証する."""
        message = f"assert_ge: {self._assert_ge} <= count: {count}"
        logger.debug(message)
        if self._assert_ge is not None and not (self._assert_ge <= count):
            raise self._new_assertion_error(message)

    def _validate_less_equal(self, count: int) -> None:
        """上限条件を検証する."""
        message = f"count: {count} <= assert_le: {self._assert_le}"
        logger.debug(message)
        if self._assert_le is not None and not (count <= self._assert_le):
            raise self._new_assertion_error(message)

    def _new_assertion_error(self, message: str) -> CommandError:
        """アサーション不成立時の例外を生成する."""
        return CommandError(return_code=message, cmd=self._mask_password())

    def dry_run(self):
        """ドライラン時の件数検証条件を出力する."""
        super().dry_run()
        logger.info("count")
        logger.debug(self._describe_assertion())

    def _describe_assertion(self) -> str:
        """現在の件数アサーション条件を文字列化する.

        Returns:
            str: アサーション条件の説明.

        Raises:
            CommandError: 条件未指定の場合.
        """
        if self._assert_eq is not None:
            return f"count == assert_eq: {self._assert_eq}"
        if self._assert_ne is not None:
            return f"count != assert_ne: {self._assert_ne}"
        if self._assert_ge is not None and self._assert_le is not None:
            if self._assert_ge <= self._assert_le:
                return f"assert_ge: {self._assert_ge} <= count <= assert_le: {self._assert_le}"
            return f"count <= assert_le: {self._assert_le} or assert_ge: {self._assert_ge} <= count"
        if self._assert_ge is not None:
            return f"assert_ge: {self._assert_ge} <= count"
        if self._assert_le is not None:
            return f"count <= assert_le: {self._assert_le}"
        raise self._new_assertion_error("Undefined assert_eq, assert_ne, assert_ge, assert_le.")

    def tear_down(self):
        """実行後処理を行う."""
        super().tear_down()
