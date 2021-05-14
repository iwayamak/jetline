# -*- coding: utf-8 -*-

import copy
import logging
from .abc.component import Component

logger = logging.getLogger('jetline')


class PluginComponent(Component):

    def __init__(self, param):
        for key, value in param.items():
            if not key == 'class':
                setattr(self, key, value)
        Component.__init__(self)

    def _validation(self):
        pass

    @classmethod
    def create_component(cls, param):
        instance = PluginComponent(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        log_dict = copy.deepcopy(instance_dict)
        log_dict['_password'] = '****'
        logger.info(f'created {cls.__name__}')
        logger.info(log_dict)
