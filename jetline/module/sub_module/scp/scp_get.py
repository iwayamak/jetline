"""SCP 取得サブモジュール。."""

from ....command.scp.scp_get_command import ScpGetCommand
from ....util.path_util import PathUtil
from ...sub_module_parameter.scp.scp_get_parameter import ScpGetParameter
from .abc.scp_sub_module import ScpSubModule


class ScpGet(ScpSubModule):
    """SCP で指定パターンのファイルをローカルへ取得する。."""

    def __init__(self, param: ScpGetParameter):
        """SCP取得サブモジュールを初期化する。.

        Args:
            param: SCP取得パラメータ。
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する。."""
        component = self.resolve_scp_component()
        object_list: list[str] = []
        PathUtil.mkdir_if_not_exists(self._parameter.local_dir_path.get())
        command = ScpGetCommand(
            component,
            self._parameter.remote_path.get(),
            self._parameter.local_dir_path.get(),
            self._parameter.recursive.get(),
            self._parameter.preserve_times.get(),
            object_list,
        )
        command.execute()
        self._result_local_file_list = object_list
