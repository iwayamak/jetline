# -*- coding: utf-8 -*-

import logging
from .abc.command import Command

logger = logging.getLogger('jetline')


class CommandQueue(object):
    """
    コマンド実行を管理するキュー
    """
    def __init__(self):
        self._command_list = []
        self._current_index = 0

    def add_command(self, command: Command):
        self._command_list.append(command)

    def execute(self):
        logger.debug('command queue executing')
        command = self._next()
        while command is not None:
            logger.debug(f'queue seq: {self._current_index}')
            command.execute()
            command = self._next()

    def _next(self):
        if self._current_index < len(self._command_list):
            command = self._command_list[self._current_index]
            self._current_index += 1
            return command
        else:
            return None
