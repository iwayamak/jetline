"""SCP コマンドの共通基底。."""

import logging
import shlex

from paramiko import AutoAddPolicy, SSHClient
from scp import SCPClient

from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class ScpCommand(Command):
    """SCP 転送を行うコマンド基底クラス。."""

    def __init__(self, component: Component):
        """SCP コマンドを初期化する。.

        Args:
            component: SCP 接続情報を持つコンポーネント。
        """
        self.ssh: SSHClient | None = None
        self.scp: SCPClient | None = None
        super().__init__(component)

    def set_up(self):
        """実行前処理を行う。."""
        super().set_up()

    def body(self):
        """実行本体の事前処理を行う。."""
        super().body()

    def run(self):
        """SCP 接続を確立する。."""
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(
            username=self.component.user,
            password=self.component.password,
            hostname=self.component.host,
            port=self.component.port,
        )
        self.scp = SCPClient(self.ssh.get_transport(), sanitize=lambda x: x)

    def list_remote_paths(self, remote_path_pattern: str) -> list[str]:
        """リモートパスを展開して一覧取得する。

        Args:
            remote_path_pattern: 展開対象のリモートパスパターン。

        Returns:
            list[str]: 展開されたリモートパス一覧。
        """
        if self.ssh is None:
            return []
        quoted_pattern = shlex.quote(remote_path_pattern)
        command = f"ls -1 {quoted_pattern}"
        _, stdout, _ = self.ssh.exec_command(command)
        return [line.strip() for line in stdout if line.strip()]

    def dry_run(self):
        """ドライラン時の処理を行う。."""
        return None

    def tear_down(self):
        """SCP/SSH 接続をクローズする。."""
        self._close_scp()
        self._close_ssh()
        super().tear_down()

    def _close_scp(self) -> None:
        """SCP クライアントを安全にクローズする。"""
        if self.scp is None:
            return
        try:
            self.scp.close()
        except Exception:
            logger.exception("failed to close scp client")
        finally:
            self.scp = None

    def _close_ssh(self) -> None:
        """SSH クライアントを安全にクローズする。"""
        if self.ssh is None:
            return
        try:
            self.ssh.close()
        except Exception:
            logger.exception("failed to close ssh client")
        finally:
            self.ssh = None
