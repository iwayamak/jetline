# -*- coding: utf-8 -*-

import logging
from jetline.command.abc.subprocess_command import SubprocessCommand

logger = logging.getLogger('jetline')


class ShellCommand(SubprocessCommand):

    def __init__(self, kwargs: dict):
        self._kwargs = kwargs
        super().__init__(None, self._kwargs['command_list'])

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        super().run()
        logger.info(self._stdout.decode('utf-8').strip())

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
