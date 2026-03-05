"""PostgreSQL COPY FROM 用パラメータ。."""

from .....validator.validator import Validator
from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue


class PostgreSQLCopyFromParameter(SubModuleParameter):
    """PostgreSQL COPY FROM 実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """PostgreSQL COPY FROM 用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._postgresql_component_key = None
        self._table_name = None
        self._column_list = None
        self._csv_file_name = None
        self._delimiter = None
        self._null_str = None
        self._header = None
        self._quote = None
        self._escape = None
        self._encoding = None
        self._gzip = None
        self._use_last_result = None
        self._remove_source_file = None
        super().__init__(params)

    @property
    def postgresql_component_key(self):
        """PostgreSQL コンポーネントキーを返す。."""
        return self._postgresql_component_key

    @postgresql_component_key.setter
    @Validator.component_key
    def postgresql_component_key(self, value):
        """PostgreSQL コンポーネントキーを設定する。."""
        self._postgresql_component_key = MustValue(value)

    @property
    def table_name(self):
        """取込先テーブル名を返す。."""
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        """取込先テーブル名を設定する。."""
        self._table_name = MustValue(value)

    @property
    def column_list(self):
        """取込対象カラム一覧を返す。."""
        return self._column_list

    @column_list.setter
    @Validator.list
    def column_list(self, value):
        """取込対象カラム一覧を設定する。."""
        self._column_list = OptionValue(value, default=None)

    @property
    def csv_file_name(self):
        """入力ファイルパターンを返す。."""
        return self._csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, value):
        """入力ファイルパターンを設定する。."""
        self._csv_file_name = OptionValue(value)

    @property
    def delimiter(self):
        """区切り文字を返す。."""
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        """区切り文字を設定する。."""
        self._delimiter = OptionValue(value, default=',')

    @property
    def null_str(self):
        """NULL 文字列表現を返す。."""
        return self._null_str

    @null_str.setter
    def null_str(self, value):
        """NULL 文字列表現を設定する。."""
        self._null_str = OptionValue(value)

    @property
    def header(self):
        """ヘッダー有無を返す。."""
        return self._header

    @header.setter
    @Validator.boolean
    def header(self, value):
        """ヘッダー有無を設定する。."""
        self._header = OptionValue(value, default=True)

    @property
    def quote(self):
        """クォート文字を返す。."""
        return self._quote

    @quote.setter
    def quote(self, value):
        """クォート文字を設定する。."""
        self._quote = OptionValue(value, default='"')

    @property
    def escape(self):
        """エスケープ文字を返す。."""
        return self._escape

    @escape.setter
    def escape(self, value):
        """エスケープ文字を設定する。."""
        self._escape = OptionValue(value, default='"')

    @property
    def encoding(self):
        """入力ファイルエンコーディングを返す。."""
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        """入力ファイルエンコーディングを設定する。."""
        self._encoding = OptionValue(value, default='utf8')

    @property
    def gzip(self):
        """Gzip 入力フラグを返す。."""
        return self._gzip

    @gzip.setter
    @Validator.boolean
    def gzip(self, value):
        """Gzip 入力フラグを設定する。."""
        self._gzip = OptionValue(value, default=False)

    @property
    def use_last_result(self):
        """直前結果再利用フラグを返す。."""
        return self._use_last_result

    @use_last_result.setter
    @Validator.boolean
    def use_last_result(self, value):
        """直前結果再利用フラグを設定する。."""
        self._use_last_result = OptionValue(value, default=False)

    @property
    def remove_source_file(self):
        """取込後にソース削除するかどうかを返す。."""
        return self._remove_source_file

    @remove_source_file.setter
    @Validator.boolean
    def remove_source_file(self, value):
        """取込後にソース削除するかどうかを設定する。."""
        self._remove_source_file = OptionValue(value, default=False)
