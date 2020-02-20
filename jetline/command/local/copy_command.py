# -*- coding: utf-8 -*-

import os
import logging
from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class CopyCommand(BuiltInCommand):

    INSTANCE_NAME = 'shutil'
    F_ATTR_NAME = 'copy'
    D_ATTR_NAME = 'copytree'

    def __init__(self, source_path, destination_path):
        self._source_path = source_path
        self._destination_path = destination_path
        logger.info(f'source_path: {self._source_path}')
        logger.info(f'destination_path: {self._destination_path}')
        if os.path.isdir(self._source_path):
            super().__init__(None, self.INSTANCE_NAME, self.D_ATTR_NAME)
        else:
            super().__init__(None, self.INSTANCE_NAME, self.F_ATTR_NAME)

    def _run_obj_attr(self):
        self._obj_attr()(self._source_path, self._destination_path)
