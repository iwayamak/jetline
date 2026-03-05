"""DB コマンドの共通基底."""

import logging
from abc import ABCMeta, abstractmethod

from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger("jetline")


class DbCommand(Command, metaclass=ABCMeta):
    """DB コマンドの共通基底クラス."""

    def __init__(self, component: Component):
        """DB コマンドを初期化する.

        Args:
            component: 利用する DB コンポーネント.
        """
        self._query = None
        self._cursor = None
        self._connection = None
        super().__init__(component)

    def set_up(self):
        """共通の実行前処理を行う."""
        super().set_up()

    def body(self):
        """実行する SQL を構築する."""
        self._query = self._query_builder()
        super().body()

    def run(self):
        """クエリ実行に必要なカーソルを準備する."""
        self._cursor = self._connection.cursor()
        logger.info("Performing queries\n%s", self._mask_password())

    def dry_run(self):
        """クエリを実行せずに内容を出力する."""
        logger.info("Dry run queries\n%s", self._mask_password())

    def tear_down(self):
        """カーソルと接続をクローズする."""
        self._close_cursor()
        self._close_connection()
        super().tear_down()

    def _close_cursor(self) -> None:
        """カーソルを安全にクローズする."""
        if self._cursor is None:
            return
        try:
            self._cursor.close()
        except Exception:
            logger.exception("Failed to close cursor")
        finally:
            self._cursor = None

    def _close_connection(self) -> None:
        """DB 接続を安全にクローズする."""
        if self._connection is None:
            return
        try:
            self._connection.close()
        except Exception:
            logger.exception("Failed to close connection")
        finally:
            self._connection = None

    @abstractmethod
    def _query_builder(self):
        """実行 SQL を組み立てる."""

    @abstractmethod
    def _mask_password(self):
        """ログ出力用に機微情報をマスクした SQL を返す."""
