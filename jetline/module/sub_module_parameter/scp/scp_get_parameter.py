"""SCP取得用パラメータ。."""

from ....validator.validator import Validator
from ..abc.sub_module_parameter import SubModuleParameter
from ..value.must_value import MustValue
from ..value.option_value import OptionValue


class ScpGetParameter(SubModuleParameter):
    """SCP 取得実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """SCP取得用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._scp_component_key = None
        self._remote_path = None
        self._local_dir_path = None
        self._recursive = None
        self._preserve_times = None
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
    def remote_path(self):
        """取得対象リモートパスを返す。."""
        return self._remote_path

    @remote_path.setter
    def remote_path(self, value):
        """取得対象リモートパスを設定する。."""
        self._remote_path = MustValue(value)

    @property
    def local_dir_path(self):
        """保存先ローカルディレクトリを返す。."""
        return self._local_dir_path

    @local_dir_path.setter
    def local_dir_path(self, value):
        """保存先ローカルディレクトリを設定する。."""
        self._local_dir_path = MustValue(value)

    @property
    def recursive(self):
        """再帰取得フラグを返す。."""
        return self._recursive

    @recursive.setter
    @Validator.boolean
    def recursive(self, value):
        """再帰取得フラグを設定する。."""
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
