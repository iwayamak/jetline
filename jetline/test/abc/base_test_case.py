# -*- coding: utf-8 -*-

import unittest
import logging.config
from ...util.path_util import PathUtil
from ...util.yaml_util import YamlUtil


logging.config.dictConfig(YamlUtil.load_file(PathUtil.logging_conf_path()))
logger = logging.getLogger('jetline')


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        logger.log_name = self.__class__.__name__
        logger.info('start')
        super(BaseTestCase, self).__init__(*args, **kwargs)
