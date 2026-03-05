"""SCP送信用パラメータ。."""

from ....validator.validator import Validator
from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ..value.option_value import OptionValue


class ScpPutParameter(SubModuleParameter):
    """SCP 送信実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """SCP送信用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._scp_component_key = None
        self._local_path = None
        self._remote_dir_path = None
        self._recursive = None
        self._preserve_times = None
        self._use_last_result = None
        super().__init__(params)

    @property
    def scp_component_key(self):
        """SCP コンポーネントキーを返す。."""
        return self._scp_component_key

    @scp_component_key.setter
    @Validator.component_key
    def scp_component_key(self, value):
        """SCP コンポーネントキーを設定する。."""
        self._scp_component_key = MustValue(value)

    @property
    def local_path(self):
        """送信対象ローカルパスを返す。."""
        return self._local_path

    @local_path.setter
    def local_path(self, value):
        """送信対象ローカルパスを設定する。."""
        self._local_path = MustValue(value)

    @property
    def remote_dir_path(self):
        """送信先リモートディレクトリを返す。."""
        return self._remote_dir_path

    @remote_dir_path.setter
    def remote_dir_path(self, value):
        """送信先リモートディレクトリを設定する。."""
        self._remote_dir_path = MustValue(value)

    @property
    def recursive(self):
        """再帰送信フラグを返す。."""
        return self._recursive

    @recursive.setter
    @Validator.boolean
    def recursive(self, value):
        """再帰送信フラグを設定する。."""
        self._recursive = OptionValue(value, default=False)

    @property
    def preserve_times(self):
        """タイムスタンプ保持フラグを返す。."""
        return self._preserve_times

    @preserve_times.setter
    @Validator.boolean
    def preserve_times(self, value):
        """タイムスタンプ保持フラグを設定する。."""
        self._preserve_times = OptionValue(value, default=False)

    @property
    def use_last_result(self):
        """直前結果再利用フラグを返す。."""
        return self._use_last_result

    @use_last_result.setter
    @Validator.boolean
    def use_last_result(self, value):
        """直前結果再利用フラグを設定する。."""
        self._use_last_result = OptionValue(value, default=False)
