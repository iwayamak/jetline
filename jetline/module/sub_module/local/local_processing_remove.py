"""ローカル削除サブモジュール。"""

import os

from ....command.command_queue import CommandQueue
from ....command.local.remove_command import RemoveCommand
from ...sub_module_parameter.local.local_processing_remove_parameter import (
    LocalProcessingRemoveParameter,
)
from .abc.local_sub_module import LocalSubModule


class LocalProcessingRemove(LocalSubModule):
    """ローカルファイル・ディレクトリを削除する。"""

    def __init__(self, param: LocalProcessingRemoveParameter):
        """ローカル削除サブモジュールを初期化する。

        Args:
            param: ローカル削除用パラメータ。
        """
        super().__init__(param)

    def run(self):
        """削除対象を展開して順次削除する。"""
        path_pattern_list = self._resolve_target_patterns()
        queue = CommandQueue()
        removed_paths: list[str] = []
        for path in self.expand_glob_patterns(path_pattern_list):
            if os.path.exists(path):
                queue.add_command(RemoveCommand(path))
                removed_paths.append(path)
        queue.execute()
        self._result_local_file_list = removed_paths

    def _resolve_target_patterns(self) -> list[str]:
        """削除対象パターンを解決する。

        Returns:
            list[str]: 削除対象パターン一覧。
        """
        if self._parameter.use_last_result.get():
            # 直前サブモジュール結果を削除対象として再利用する。
            return self.get_last_result_local_paths()
        return self.normalize_non_empty_paths(self._parameter.path_list.get())
