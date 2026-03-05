"""PostgreSQL COPY TO 用パラメータ。."""

from .....validator.validator import Validator
from ...abc.sub_module_parameter import SubModuleParameter
from ...value.must_value import MustValue
from ...value.option_value import OptionValue


class PostgreSQLCopyToParameter(SubModuleParameter):
    """PostgreSQL COPY TO 実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """PostgreSQL COPY TO 用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._postgresql_component_key = None
        self._sql_file_name = None
        self._csv_file_name = None
        self._delimiter = None
        self._null_str = None
        self._header = None
        self._quote = None
        self._escape = None
        self._force_quote_list = None
        self._encoding = None
        self._gzip = None
        self._input_value = None
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
    def sql_file_name(self):
        """抽出 SQL ファイルパスを返す。."""
        return self._sql_file_name

    @sql_file_name.setter
    @Validator.path
    def sql_file_name(self, value):
        """抽出 SQL ファイルパスを設定する。."""
        self._sql_file_name = MustValue(value)

    @property
    def csv_file_name(self):
        """出力先 CSV ファイル名を返す。."""
        return self._csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, value):
        """出力先 CSV ファイル名を設定する。."""
        self._csv_file_name = MustValue(value)

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
        """ヘッダー出力有無を返す。."""
        return self._header

    @header.setter
    @Validator.boolean
    def header(self, value):
        """ヘッダー出力有無を設定する。."""
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
    def force_quote_list(self):
        """強制クォート対象カラム一覧を返す。."""
        return self._force_quote_list

    @force_quote_list.setter
    @Validator.list
    def force_quote_list(self, value):
        """強制クォート対象カラム一覧を設定する。."""
        self._force_quote_list = OptionValue(value)

    @property
    def encoding(self):
        """出力ファイルエンコーディングを返す。."""
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        """出力ファイルエンコーディングを設定する。."""
        self._encoding = OptionValue(value, default='utf-8')

    @property
    def gzip(self):
        """Gzip 出力フラグを返す。."""
        return self._gzip

    @gzip.setter
    @Validator.boolean
    def gzip(self, value):
        """Gzip 出力フラグを設定する。."""
        self._gzip = OptionValue(value, default=False)

    @property
    def input_value(self):
        """SQL テンプレートへ渡す入力値辞書を返す。."""
        return self._input_value

    @input_value.setter
    @Validator.dict
    def input_value(self, value):
        """SQL テンプレートへ渡す入力値辞書を設定する。."""
        self._input_value = OptionValue(value)
