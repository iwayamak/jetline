"""PostgreSQL 件数検証付き SQL 実行用パラメータ."""

from .....validator.validator import Validator
from ...value.option_value import OptionValue
from .postgresql_processing_parameter import PostgreSQLProcessingParameter


class PostgreSQLProcessingCountParameter(PostgreSQLProcessingParameter):
    """件数検証付き SQL 実行の入力パラメータを保持する."""

    def __init__(self, params: dict | None = None):
        """件数検証付き SQL 実行用パラメータを初期化する.

        Args:
            params: パラメータ辞書.
        """
        self._assert_eq = None
        self._assert_ne = None
        self._assert_ge = None
        self._assert_le = None
        super().__init__(params)

    @property
    def assert_eq(self):
        """件数一致条件を返す."""
        return self._assert_eq

    @assert_eq.setter
    @Validator.digit
    def assert_eq(self, value):
        """件数一致条件を設定する."""
        self._assert_eq = OptionValue(self._to_int_or_none(value))

    @property
    def assert_ne(self):
        """件数不一致条件を返す."""
        return self._assert_ne

    @assert_ne.setter
    @Validator.digit
    def assert_ne(self, value):
        """件数不一致条件を設定する."""
        self._assert_ne = OptionValue(self._to_int_or_none(value))

    @property
    def assert_ge(self):
        """件数下限条件を返す."""
        return self._assert_ge

    @assert_ge.setter
    @Validator.digit
    def assert_ge(self, value):
        """件数下限条件を設定する."""
        self._assert_ge = OptionValue(self._to_int_or_none(value))

    @property
    def assert_le(self):
        """件数上限条件を返す."""
        return self._assert_le

    @assert_le.setter
    @Validator.digit
    def assert_le(self, value):
        """件数上限条件を設定する."""
        self._assert_le = OptionValue(self._to_int_or_none(value))

    @staticmethod
    def _to_int_or_none(value: int | str | None) -> int | None:
        """値を `int` へ正規化する.

        Args:
            value: 入力値.

        Returns:
            int | None: `None` はそのまま、それ以外は `int` へ変換した値.
        """
        if value is None:
            return None
        return int(value)
