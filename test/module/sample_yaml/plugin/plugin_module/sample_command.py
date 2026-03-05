"""サンプル CustomCommand 実装."""

import logging

from jetline.command.abc.custom_command import CustomCommand

logger = logging.getLogger("jetline")


class SampleCommand(CustomCommand):
    """カスタムコマンドのライフサイクルを確認するサンプル実装."""

    def set_up(self) -> None:
        """実行前フックを呼び出してログ出力する."""
        super().set_up()
        logger.debug("Command set_up")

    def body(self) -> None:
        """本体フックを呼び出してログ出力する."""
        super().body()
        logger.debug("Command body")

    def run(self) -> None:
        """実行フックを呼び出し、受け取った引数をログへ出す."""
        super().run()
        logger.debug("Command run")
        logger.debug({"key1": self._kwargs["key1"]})

    def dry_run(self) -> None:
        """Dry-run フックを呼び出してログ出力する."""
        super().dry_run()
        logger.debug("Command dry_run")

    def tear_down(self) -> None:
        """後処理フックを呼び出してログ出力する."""
        super().tear_down()
        logger.debug("Command tear_down")
