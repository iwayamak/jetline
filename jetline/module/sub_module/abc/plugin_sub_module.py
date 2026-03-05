"""Plugin サブモジュールの共通基底."""

import logging

from .sub_module import SubModule

logger = logging.getLogger("jetline")


class PluginSubModule(SubModule):
    """プラグイン系サブモジュールの共通処理を提供する基底クラス."""

    def set_up(self):
        """実行前処理として共通コンテキストをログ出力する."""
        super().set_up()
        logger.info(
            "Executing %s (plugin_path=%s, package=%s, class_name=%s)",
            self.__class__.__name__,
            self._parameter.plugin_path.get(),
            self._parameter.package.get(),
            self._parameter.class_name.get(),
        )
