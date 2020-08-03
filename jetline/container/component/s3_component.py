# -*- coding: utf-8 -*-

import copy
import logging
from .abc.component import Component

logger = logging.getLogger('jetline')


class S3Component(Component):

    def __init__(self, param):
        self._bucket = param.get('bucket')
        self._aws_access_key = param.get('aws_access_key')
        self._aws_secret_access_key = param.get('aws_secret_access_key')
        self._region_name = param.get('region_name')
        Component.__init__(self)

    def _validation(self):
        if self._bucket is None or self._aws_access_key is None or \
                self._aws_secret_access_key is None or self._region_name is None:
            raise Exception(
                'bucket / aws_access_key / aws_secret_access_key / region_name is None!'
            )

    @property
    def bucket(self):
        return self._bucket

    @property
    def aws_access_key(self):
        return self._aws_access_key

    @property
    def aws_secret_access_key(self):
        return self._aws_secret_access_key

    @property
    def region_name(self):
        return self._region_name

    @classmethod
    def create_component(cls, param):
        instance = S3Component(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        log_dict = copy.deepcopy(instance_dict)
        log_dict["_aws_secret_access_key"] = '****'
        logger.info(f'created {cls.__name__}')
        logger.info(log_dict)
