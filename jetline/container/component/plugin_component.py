"""プラグインコンポーネント実装。."""

import copy
import logging

from .abc.component import Component

logger = logging.getLogger("jetline")


class PluginComponent(Component):
    """プラグイン設定を保持するコンポーネント。."""

    def __init__(self, param: dict):
        """プラグイン設定を属性へ展開して初期化する。.

        Args:
            param: コンポーネント設定辞書。
        """
        for key, value in param.items():
            if key != "class":
                setattr(self, key, value)
        super().__init__()

    def _validation(self):
        """プラグイン設定の妥当性を検証する。."""

    @classmethod
    def create_component(cls, param: dict) -> "PluginComponent":
        """設定辞書からコンポーネントを生成する。."""
        instance = cls(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        """マスク済み情報をログ出力する。."""
        log_dict = copy.deepcopy(instance_dict)
        if "_password" in log_dict:
            log_dict["_password"] = "****"
        logger.info("created %s", cls.__name__)
        logger.info(log_dict)
