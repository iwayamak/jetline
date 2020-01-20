# -*- coding: utf-8 -*-

import logging
from jetline.command.abc.custom_command import CustomCommand

logger = logging.getLogger('jetline')


class SampleCommand(CustomCommand):

    def set_up(self):
        super().set_up()
        logger.debug('Command set_up')

    def body(self):
        super().body()
        logger.debug('Command body')

    def run(self):
        super().run()
        logger.debug('Command run')
        logger.debug({'key1': self._kwargs['key1']})

    def dry_run(self):
        super().dry_run()
        logger.debug('Command dry_run')

    def tear_down(self):
        super().tear_down()
        logger.debug('Command tear_down')
