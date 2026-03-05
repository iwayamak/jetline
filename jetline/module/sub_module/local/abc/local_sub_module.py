"""ローカル処理サブモジュールの共通基底."""

import logging

from ...abc.sub_module import SubModule

logger = logging.getLogger("jetline")


class LocalSubModule(SubModule):
    """ローカル処理系サブモジュールの共通処理を提供する基底クラス."""

    def set_up(self):
        """実行前処理として共通コンテキストをログ出力する."""
        super().set_up()
        logger.info("Executing %s", self.__class__.__name__)
