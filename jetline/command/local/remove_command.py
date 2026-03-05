"""ローカルファイル・ディレクトリ削除コマンド。."""

import logging
import os
from collections.abc import Callable
from typing import Any

from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class RemoveCommand(BuiltInCommand):
    """`os.remove` / `shutil.rmtree` を切り替えて実行する。."""

    FILE_INSTANCE_NAME = 'os'
    FILE_ATTR_NAME = 'remove'
    DIR_INSTANCE_NAME = 'shutil'
    DIR_ATTR_NAME = 'rmtree'

    def __init__(self, remove_path: str):
        """削除コマンドを初期化する。.

        Args:
            remove_path: 削除対象パス。
        """
        self._remove_path = remove_path
        logger.info(f'remove_path: {self._remove_path}')
        if os.path.isdir(remove_path):
            super().__init__(None, self.DIR_INSTANCE_NAME, self.DIR_ATTR_NAME)
        else:
            super().__init__(None, self.FILE_INSTANCE_NAME, self.FILE_ATTR_NAME)

    def _run_target_callable(self, target_callable: Callable[..., Any]) -> None:
        """削除処理を実行する。."""
        target_callable(self._remove_path)
