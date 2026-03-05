"""SCP 取得コマンド。."""

import logging
from collections.abc import MutableSequence

from ...container.component.scp_component import ScpComponent
from .abc.scp_command import ScpCommand

logger = logging.getLogger('jetline')


class ScpGetCommand(ScpCommand):
    """リモートファイルをローカルへ取得する。."""

    def __init__(
        self,
        component: ScpComponent,
        remote_path: str,
        local_dir_path: str,
        recursive: bool,
        preserve_times: bool,
        object_list: MutableSequence[str],
    ):
        """SCP 取得コマンドを初期化する。.

        Args:
            component: SCP コンポーネント。
            remote_path: 取得元パス（ワイルドカード可）。
            local_dir_path: 取得先ローカルディレクトリ。
            recursive: 再帰取得するかどうか。
            preserve_times: タイムスタンプを保持するかどうか。
            object_list: 取得ファイル一覧の格納先。
        """
        self._remote_path = remote_path
        self._local_dir_path = local_dir_path
        self._recursive = recursive
        self._preserve_times = preserve_times
        self._object_list = object_list
        super().__init__(component)

    def run(self):
        """SCP でファイルを取得し、取得対象一覧を格納する。."""
        super().run()
        self.scp.get(
            remote_path=self._remote_path,
            local_path=self._local_dir_path,
            recursive=self._recursive,
            preserve_times=self._preserve_times,
        )
        remote_paths = self.list_remote_paths(self._remote_path)
        self._object_list.clear()
        self._object_list.extend(remote_paths)
        logger.info("Get %s using SCP from %s", self._object_list, self.component.host)
