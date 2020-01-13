# -*- coding: utf-8 -*-

import logging
from jetline.command.abc.custom_command import CustomCommand

logger = logging.getLogger('jetline')


class SampleCommand(CustomCommand):

    def set_up(self):
        logger.debug('Command set_up')

    def body(self):
        logger.debug('Command body')

    def run(self):
        logger.debug('Command run')

    def dry_run(self):
        logger.debug('Command dry_run')

    def tear_down(self):
        logger.debug('Command tear_down')
