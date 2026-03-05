"""S3 取得サブモジュール。"""

import os

from ....command.command_queue import CommandQueue
from ....command.local.touch_file_command import TouchFileCommand
from ....command.s3.s3_get_command import S3GetCommand
from ...sub_module_parameter.s3.s3_get_parameter import S3GetParameter
from .abc.s3_sub_module import S3SubModule


class S3Get(S3SubModule):
    """ワイルドカード指定で S3 オブジェクトを取得する。"""

    def __init__(self, param: S3GetParameter):
        """S3取得サブモジュールを初期化する。

        Args:
            param: S3取得パラメータ。
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する。"""
        queue = CommandQueue()
        s3_file_pattern = self._parameter.s3_file_path.get()
        matched_objects = self.list_objects_by_pattern(s3_file_pattern)
        file_path_list = self.extract_keys(matched_objects)
        component = self.resolve_s3_component()

        downloaded_file_list: list[str] = []
        for file_path in file_path_list:
            local_path = os.path.join(
                self._parameter.local_dir_path.get(),
                os.path.basename(file_path),
            )
            queue.add_command(S3GetCommand(component, file_path, local_path))
            downloaded_file_list.append(local_path)

        end_file_name = self._parameter.end_file_name.get()
        if end_file_name is not None:
            queue.add_command(TouchFileCommand(end_file_name))
            downloaded_file_list.append(end_file_name)
        queue.execute()
        self._result_local_file_list = downloaded_file_list
