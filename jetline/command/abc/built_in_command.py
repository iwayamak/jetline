# -*- coding: utf-8 -*-

from typing import Union
import logging
import importlib
from abc import ABCMeta, abstractmethod
from ..abc.command import Command
from ...container.component.abc.component import Component

logger = logging.getLogger('jetline')


class BuiltInCommand(Command, metaclass=ABCMeta):

    def __init__(self, component: Union[Component, None],
                 instance_name: str, attr_name: str):
        self._instance_name = instance_name
        self._attr_name = attr_name
        super(BuiltInCommand, self).__init__(component)

    def set_up(self):
        pass

    def body(self):
        pass

    def run(self):
        logger.info(
            f'instance_name: {self._instance_name}  attr_name: {str(self._attr_name)}'
        )
        self._run_obj_attr()

    def dry_run(self):
        logger.info(
            f'instance_name: {str(self._instance_name)}  attr_name: {str(self._attr_name)}'
        )

    def tear_down(self):
        pass

    def _obj_attr(self):
        obj = importlib.import_module(self._instance_name)
        return getattr(obj, self._attr_name)

    @abstractmethod
    def _run_obj_attr(self):
        pass
