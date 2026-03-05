"""S3 送信サブモジュール。"""

import os

from ....command.command_queue import CommandQueue
from ....command.local.touch_file_command import TouchFileCommand
from ....command.s3.s3_put_command import S3PutCommand
from ...sub_module_parameter.s3.s3_put_parameter import S3PutParameter
from .abc.s3_sub_module import S3SubModule


class S3Put(S3SubModule):
    """ワイルドカード展開したローカルファイルを S3 へアップロードする。"""

    def __init__(self, param: S3PutParameter):
        """S3送信サブモジュールを初期化する。

        Args:
            param: S3送信パラメータ。
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する。"""
        component = self.resolve_s3_component()
        queue = CommandQueue()
        file_path_list = self.expand_glob_patterns(
            [self._parameter.local_file_path.get()],
            recursive=True,
        )

        end_file_name = self._parameter.end_file_name.get()
        if end_file_name is not None:
            queue.add_command(TouchFileCommand(end_file_name))
            file_path_list.append(end_file_name)

        uploaded_s3_keys: list[str] = []
        for file_path in file_path_list:
            s3_key = os.path.join(self._parameter.s3_dir_path.get(), os.path.basename(file_path))
            queue.add_command(S3PutCommand(component, file_path, s3_key))
            uploaded_s3_keys.append(s3_key)
        queue.execute()
        self._result_local_file_list = file_path_list
        self._result_s3_file_list = uploaded_s3_keys
