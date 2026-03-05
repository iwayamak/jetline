"""ローカルファイル・ディレクトリコピーコマンド。."""

import logging
import os
from collections.abc import Callable
from typing import Any

from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class CopyCommand(BuiltInCommand):
    """`shutil.copy` / `shutil.copytree` を切り替えて実行する。."""

    INSTANCE_NAME = 'shutil'
    FILE_COPY_ATTR_NAME = 'copy'
    DIR_COPY_ATTR_NAME = 'copytree'

    def __init__(self, source_path: str, destination_path: str):
        """コピーコマンドを初期化する。.

        Args:
            source_path: コピー元パス。
            destination_path: コピー先パス。
        """
        self._source_path = source_path
        self._destination_path = destination_path
        logger.info(f'source_path: {self._source_path}')
        logger.info(f'destination_path: {self._destination_path}')
        attr_name = (
            self.DIR_COPY_ATTR_NAME
            if os.path.isdir(source_path)
            else self.FILE_COPY_ATTR_NAME
        )
        super().__init__(None, self.INSTANCE_NAME, attr_name)

    def _run_target_callable(self, target_callable: Callable[..., Any]) -> None:
        """コピー処理を実行する。."""
        target_callable(self._source_path, self._destination_path)
