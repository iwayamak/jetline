# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from ..abc.command import Command


class CustomCommand(Command, metaclass=ABCMeta):

    def __init__(self, kwargs: dict):
        self._kwargs = kwargs
        super().__init__(None)

    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def body(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def dry_run(self):
        pass

    @abstractmethod
    def tear_down(self):
        pass
