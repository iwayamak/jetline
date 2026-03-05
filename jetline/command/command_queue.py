"""コマンドキュー実行を提供する。."""

import logging
from collections.abc import Iterator

from .abc.command import Command

logger = logging.getLogger('jetline')


class CommandQueue:
    """コマンド実行を管理するキュー。."""

    def __init__(self):
        """空のコマンドキューを初期化する。."""
        self._command_list: list[Command] = []
        self._current_index = 0

    def add_command(self, command: Command) -> None:
        """キュー末尾にコマンドを追加する。

        Args:
            command: 追加するコマンド。
        """
        self._command_list.append(command)

    def execute(self, reset_index: bool = False) -> None:
        """キューに積まれたコマンドを順に実行する。

        Args:
            reset_index: True の場合、先頭から再実行する。
        """
        if reset_index:
            self.reset()
        logger.debug('command queue executing')
        for command in self.iter_remaining():
            logger.debug('queue seq: %s', self._current_index)
            command.execute()

    def reset(self) -> None:
        """実行インデックスのみ先頭に戻す。"""
        self._current_index = 0

    def clear(self) -> None:
        """キュー内容と実行インデックスを初期化する。"""
        self._command_list = []
        self._current_index = 0

    def __len__(self) -> int:
        """登録コマンド数を返す。"""
        return len(self._command_list)

    def _next(self) -> Command | None:
        """次のコマンドを返し、カーソルを進める。."""
        if self._current_index < len(self._command_list):
            command = self._command_list[self._current_index]
            self._current_index += 1
            return command
        return None

    def iter_remaining(self) -> Iterator[Command]:
        """未実行コマンドを順に返す。."""
        while True:
            command = self._next()
            if command is None:
                break
            yield command
