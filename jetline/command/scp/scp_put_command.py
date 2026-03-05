"""SCP 送信コマンド。."""

import logging
from collections.abc import Sequence

from ...container.component.scp_component import ScpComponent
from .abc.scp_command import ScpCommand

logger = logging.getLogger('jetline')


class ScpPutCommand(ScpCommand):
    """ローカルファイルをリモートへ送信する。."""

    def __init__(
        self,
        component: ScpComponent,
        local_path_list: Sequence[str],
        remote_dir_path: str,
        recursive: bool,
        preserve_times: bool,
    ):
        """SCP 送信コマンドを初期化する。.

        Args:
            component: SCP コンポーネント。
            local_path_list: 送信対象のローカルパス一覧。
            remote_dir_path: 送信先リモートディレクトリ。
            recursive: 再帰転送するかどうか。
            preserve_times: タイムスタンプを保持するかどうか。
        """
        self._local_path_list = list(local_path_list)
        self._remote_dir_path = remote_dir_path
        self._recursive = recursive
        self._preserve_times = preserve_times
        super().__init__(component)

    def run(self):
        """SCP でファイルを送信する。."""
        super().run()
        self.scp.put(
            files=self._local_path_list,
            remote_path=self._remote_dir_path,
            recursive=self._recursive,
            preserve_times=self._preserve_times,
        )
        logger.info("Put %s using SCP to %s", self._local_path_list, self.scp_component.host)
