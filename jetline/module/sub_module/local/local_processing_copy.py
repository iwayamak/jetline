"""ローカルコピーサブモジュール。."""

from ....command.local.copy_command import CopyCommand
from ...sub_module_parameter.local.local_processing_copy_parameter import (
    LocalProcessingCopyParameter,
)
from .abc.local_sub_module import LocalSubModule


class LocalProcessingCopy(LocalSubModule):
    """ローカルパスをコピーする。."""

    def __init__(self, param: LocalProcessingCopyParameter):
        """ローカルコピーサブモジュールを初期化する。.

        Args:
            param: ローカルコピー用パラメータ。
        """
        super().__init__(param)

    def run(self):
        """コピー処理を実行する。."""
        source_path = self._parameter.source_path.get()
        destination_path = self._parameter.destination_path.get()
        command = CopyCommand(source_path, destination_path)
        command.execute()
        self._result_local_file_list = [destination_path]
