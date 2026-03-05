"""ローカル touch コマンド。."""

import logging
from collections.abc import Callable
from typing import Any

from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class TouchFileCommand(BuiltInCommand):
    """ファイルを作成し、更新時刻を現在時刻へ更新する。."""

    INSTANCE_NAME = 'os'
    ATTR_NAME = 'utime'

    def __init__(self, touch_file: str):
        """Touch コマンドを初期化する。.

        Args:
            touch_file: 作成または更新するファイルパス。
        """
        self._touch_file_path = touch_file
        logger.info(f'touch_file: {self._touch_file_path}')
        super().__init__(None, self.INSTANCE_NAME, self.ATTR_NAME)

    def _run_target_callable(self, target_callable: Callable[..., Any]) -> None:
        """ファイル作成と時刻更新を実行する。."""
        with open(self._touch_file_path, 'a', encoding='utf-8'):
            target_callable(self._touch_file_path)
