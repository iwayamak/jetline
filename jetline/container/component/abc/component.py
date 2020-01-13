# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Component(metaclass=ABCMeta):

    def __init__(self):
        self._validation()

    @abstractmethod
    def _validation(self):
        pass

    @classmethod
    @abstractmethod
    def create_component(cls, param):
        pass

    @classmethod
    @abstractmethod
    def _output_log(cls, instance):
        pass
