"""ローカルコピー用パラメータ。."""

from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue


class LocalProcessingCopyParameter(SubModuleParameter):
    """ローカルコピー実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """ローカルコピー用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._source_path = None
        self._destination_path = None
        super().__init__(params)

    @property
    def source_path(self):
        """コピー元パスを返す。."""
        return self._source_path

    @source_path.setter
    def source_path(self, value):
        """コピー元パスを設定する。."""
        self._source_path = MustValue(value)

    @property
    def destination_path(self):
        """コピー先パスを返す。."""
        return self._destination_path

    @destination_path.setter
    def destination_path(self, value):
        """コピー先パスを設定する。."""
        self._destination_path = MustValue(value)
