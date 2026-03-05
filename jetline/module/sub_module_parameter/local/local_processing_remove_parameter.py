"""ローカル削除用パラメータ。."""

from ....validator.validator import Validator
from ..abc.sub_module_parameter import SubModuleParameter
from ..value.option_value import OptionValue


class LocalProcessingRemoveParameter(SubModuleParameter):
    """ローカル削除実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """ローカル削除用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._path_list = None
        self._use_last_result = None
        super().__init__(params)

    @property
    def path_list(self):
        """削除対象パターン一覧を返す。."""
        return self._path_list

    @path_list.setter
    @Validator.list
    def path_list(self, value):
        """削除対象パターン一覧を設定する。."""
        self._path_list = OptionValue(value)

    @property
    def use_last_result(self):
        """直前結果再利用フラグを返す。."""
        return self._use_last_result

    @use_last_result.setter
    @Validator.boolean
    def use_last_result(self, value):
        """直前結果再利用フラグを設定する。."""
        self._use_last_result = OptionValue(value, default=False)
