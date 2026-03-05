"""PostgreSQL 汎用 SQL 実行用パラメータ."""

from .....validator.validator import Validator
from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue


class PostgreSQLProcessingParameter(SubModuleParameter):
    """PostgreSQL SQL 実行の入力パラメータを保持する."""

    def __init__(self, params: dict | None = None):
        """PostgreSQL SQL 実行用パラメータを初期化する.

        Args:
            params: パラメータ辞書.
        """
        self._postgresql_component_key = None
        self._sql_file_name = None
        self._input_value = None
        super().__init__(params)

    @property
    def postgresql_component_key(self):
        """PostgreSQL コンポーネントキーを返す."""
        return self._postgresql_component_key

    @postgresql_component_key.setter
    @Validator.component_key
    def postgresql_component_key(self, value):
        """PostgreSQL コンポーネントキーを設定する."""
        self._postgresql_component_key = MustValue(value)

    @property
    def sql_file_name(self):
        """SQL ファイルパスを返す."""
        return self._sql_file_name

    @sql_file_name.setter
    @Validator.path
    def sql_file_name(self, value):
        """SQL ファイルパスを設定する."""
        self._sql_file_name = MustValue(value)

    @property
    def input_value(self):
        """SQL テンプレートへ渡す入力値辞書を返す."""
        return self._input_value

    @input_value.setter
    @Validator.dict
    def input_value(self, value):
        """SQL テンプレートへ渡す入力値辞書を設定する."""
        self._input_value = OptionValue(value)
