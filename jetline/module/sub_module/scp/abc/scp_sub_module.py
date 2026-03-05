"""SCP サブモジュールの共通基底."""

import logging

from ...abc.sub_module import SubModule

logger = logging.getLogger("jetline")


class ScpSubModule(SubModule):
    """SCP 系サブモジュールの共通処理を提供する基底クラス."""

    def set_up(self):
        """実行前処理として共通コンテキストをログ出力する."""
        super().set_up()
        logger.info(
            "Executing %s (component_key=%s)",
            self.__class__.__name__,
            self._parameter.scp_component_key.get(),
        )

    def resolve_scp_component(self):
        """パラメータのコンポーネントキーから SCP コンポーネントを解決する."""
        return self.resolve_component(self._parameter.scp_component_key.get())
