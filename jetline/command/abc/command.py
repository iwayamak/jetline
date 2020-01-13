# -*- coding: utf-8 -*-

import logging
from typing import Union
from abc import ABCMeta, abstractmethod
from ...share_parameter.share_parameter import ShareParameter
from ...container.component.abc.component import Component

logger = logging.getLogger('jetline')


class Command(metaclass=ABCMeta):

    def __init__(self, component: Union[Component, None]):
        self.component = component

    @abstractmethod
    def set_up(self):
        logger.debug('jetline Command set_up')

    @abstractmethod
    def body(self):
        logger.debug('jetline Command body')

    @abstractmethod
    def run(self):
        logger.debug('jetline Command run')

    @abstractmethod
    def dry_run(self):
        logger.debug('jetline Command dry run')

    @abstractmethod
    def tear_down(self):
        logger.debug('jetline Command tear down')

    def execute(self):
        try:
            self.set_up()
            self.body()
            if ShareParameter.dry_run_mode:
                self.dry_run()
            else:
                self.run()
        finally:
            self.tear_down()
