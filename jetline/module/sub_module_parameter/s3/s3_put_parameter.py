"""S3送信用パラメータ。."""

from ....validator.validator import Validator
from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ..value.option_value import OptionValue


class S3PutParameter(SubModuleParameter):
    """S3 送信実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """S3送信用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._s3_component_key = None
        self._local_file_path = None
        self._s3_dir_path = None
        self._end_file_name = None
        super().__init__(params)

    @property
    def s3_component_key(self):
        """S3 コンポーネントキーを返す。."""
        return self._s3_component_key

    @s3_component_key.setter
    @Validator.component_key
    def s3_component_key(self, value):
        """S3 コンポーネントキーを設定する。."""
        self._s3_component_key = MustValue(value)

    @property
    def local_file_path(self):
        """送信対象ローカルファイルパターンを返す。."""
        return self._local_file_path

    @local_file_path.setter
    def local_file_path(self, value):
        """送信対象ローカルファイルパターンを設定する。."""
        self._local_file_path = MustValue(value)

    @property
    def s3_dir_path(self):
        """送信先 S3 ディレクトリを返す。."""
        return self._s3_dir_path

    @s3_dir_path.setter
    def s3_dir_path(self, value):
        """送信先 S3 ディレクトリを設定する。."""
        self._s3_dir_path = MustValue(value)

    @property
    def end_file_name(self):
        """終端ファイル名を返す。."""
        return self._end_file_name

    @end_file_name.setter
    def end_file_name(self, value):
        """終端ファイル名を設定する。."""
        self._end_file_name = OptionValue(value, default=None)
