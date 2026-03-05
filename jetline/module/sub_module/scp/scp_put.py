"""SCP 送信サブモジュール。"""

from ....command.scp.scp_put_command import ScpPutCommand
from ...sub_module_parameter.scp.scp_put_parameter import ScpPutParameter
from .abc.scp_sub_module import ScpSubModule


class ScpPut(ScpSubModule):
    """ローカルファイルをリモートディレクトリへ転送する。"""

    def __init__(self, param: ScpPutParameter):
        """SCP送信サブモジュールを初期化する。

        Args:
            param: SCP送信パラメータ。
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する。"""
        local_path_list = self._resolve_local_paths()
        component = self.resolve_scp_component()
        command = ScpPutCommand(
            component,
            local_path_list,
            self._parameter.remote_dir_path.get(),
            self._parameter.recursive.get(),
            self._parameter.preserve_times.get(),
        )
        command.execute()
        self._result_local_file_list = local_path_list

    def _resolve_local_paths(self) -> list[str]:
        """送信対象ローカルパス一覧を解決する。

        Returns:
            list[str]: 送信対象のローカルパス一覧。
        """
        if self._parameter.use_last_result.get():
            # 直前サブモジュール結果を入力ファイルとして再利用する。
            return self.get_last_result_local_paths()
        return self.expand_glob_patterns([self._parameter.local_path.get()])
