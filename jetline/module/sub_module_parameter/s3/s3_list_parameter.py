"""S3一覧取得用パラメータ。."""

from ....validator.validator import Validator
from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue


class S3ListParameter(SubModuleParameter):
    """S3 一覧取得実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """S3一覧取得用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._s3_component_key = None
        self._s3_file_path = None
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
    def s3_file_path(self):
        """一覧取得対象の S3 パスパターンを返す。."""
        return self._s3_file_path

    @s3_file_path.setter
    def s3_file_path(self, value):
        """一覧取得対象の S3 パスパターンを設定する。."""
        self._s3_file_path = MustValue(value)
