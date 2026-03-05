"""プラグインサブモジュール。."""

import importlib
import logging
import sys
from collections.abc import Mapping
from pathlib import Path

from ..sub_module_parameter.plugin_parameter import PluginParameter
from .abc.plugin_sub_module import PluginSubModule

logger = logging.getLogger("jetline")


class Plugin(PluginSubModule):
    """任意プラグインを動的ロードして実行する。."""

    def __init__(self, param: PluginParameter):
        """プラグインサブモジュールを初期化する。."""
        super().__init__(param)

    def run(self):
        """プラグインをロードして `execute()` を呼び出す。."""
        self._ensure_plugin_path()
        plugin_class = self._resolve_plugin_class()
        kwargs = self._resolve_plugin_kwargs()
        plugin = plugin_class(kwargs)
        plugin.execute()

    def _ensure_plugin_path(self) -> None:
        """プラグイン探索パスを `sys.path` に追加する。."""
        plugin_path = str(Path(self._parameter.plugin_path.get()).resolve())
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)
            logger.debug("Added plugin path to sys.path: %s", plugin_path)

    def _resolve_plugin_class(self):
        """実行対象のプラグインクラスを解決する."""
        package = self._parameter.package.get()
        class_name = self._parameter.class_name.get()
        module = importlib.import_module(package)
        return getattr(module, class_name)

    def _resolve_plugin_kwargs(self) -> dict:
        """プラグインへ渡す kwargs を辞書として返す。."""
        kwargs = self._parameter.kwargs.get()
        if kwargs is None:
            return {}
        if isinstance(kwargs, Mapping):
            return dict(kwargs)
        return {}
