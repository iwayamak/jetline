"""プラグイン実行用パラメータ。."""

from ...validator.validator import Validator
from .abc.sub_module_parameter import SubModuleParameter
from .value.must_value import MustValue
from .value.option_value import OptionValue


class PluginParameter(SubModuleParameter):
    """プラグイン実行の入力パラメータを保持する。."""

    def __init__(self, params: dict | None = None):
        """プラグイン用パラメータを初期化する。.

        Args:
            params: パラメータ辞書。
        """
        self._plugin_path = None
        self._package = None
        self._class_name = None
        self._kwargs = None
        super().__init__(params)

    @property
    def plugin_path(self):
        """プラグイン配置ディレクトリを返す。."""
        return self._plugin_path

    @plugin_path.setter
    @Validator.path
    def plugin_path(self, value):
        """プラグイン配置ディレクトリを設定する。."""
        self._plugin_path = MustValue(value)

    @property
    def package(self):
        """プラグインパッケージ名を返す。."""
        return self._package

    @package.setter
    def package(self, value):
        """プラグインパッケージ名を設定する。."""
        self._package = MustValue(value)

    @property
    def class_name(self):
        """プラグインクラス名を返す。."""
        return self._class_name

    @class_name.setter
    def class_name(self, value):
        """プラグインクラス名を設定する。."""
        self._class_name = MustValue(value)

    @property
    def kwargs(self):
        """プラグインへ渡す追加引数辞書を返す。."""
        return self._kwargs

    @kwargs.setter
    @Validator.dict
    def kwargs(self, value):
        """プラグインへ渡す追加引数辞書を設定する。."""
        self._kwargs = OptionValue(value)
