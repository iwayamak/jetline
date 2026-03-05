"""サブプロセス実行を行うサンプルコマンド."""

import logging

from jetline.command.abc.subprocess_command import SubprocessCommand

logger = logging.getLogger("jetline")


class ShellCommand(SubprocessCommand):
    """任意コマンドを実行して標準出力をログへ出す."""

    def __init__(self, kwargs: dict):
        """実行するコマンド配列を初期化する.

        Args:
            kwargs: `command_list` を含む設定.
        """
        self._kwargs = kwargs
        super().__init__(None, self._kwargs["command_list"])

    def set_up(self) -> None:
        """実行前フックを呼び出す."""
        super().set_up()

    def body(self) -> None:
        """本体フックを呼び出す."""
        super().body()

    def run(self) -> None:
        """コマンドを実行し標準出力をログへ記録する."""
        super().run()
        logger.info(self.stdout.decode("utf-8").strip())

    def dry_run(self) -> None:
        """Dry-run フックを呼び出す."""
        super().dry_run()

    def tear_down(self) -> None:
        """後処理フックを呼び出す."""
        super().tear_down()
