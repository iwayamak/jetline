# -*- coding: utf-8 -*-

import logging
from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class TouchFileCommand(BuiltInCommand):

    INSTANCE_NAME = 'os'
    ATTR_NAME = 'utime'

    def __init__(self, touch_file):
        self._touch_file_path = touch_file
        logger.info(f'touch_file: {self._touch_file_path}')
        super().__init__(None, self.INSTANCE_NAME, self.ATTR_NAME)

    def _run_obj_attr(self):
        with open(self._touch_file_path, 'a'):
            self._obj_attr()(self._touch_file_path)
