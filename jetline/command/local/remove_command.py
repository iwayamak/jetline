# -*- coding: utf-8 -*-

import os
import logging
from ..abc.built_in_command import BuiltInCommand

logger = logging.getLogger('jetline')


class RemoveCommand(BuiltInCommand):

    F_INSTANCE_NAME = 'os'
    F_ATTR_NAME = 'remove'

    D_INSTANCE_NAME = 'shutil'
    D_ATTR_NAME = 'rmtree'

    def __init__(self, remove_path):
        self._remove_path = remove_path
        logger.info(f'remove_path: {self._remove_path}')
        if os.path.isdir(self._remove_path):
            super().__init__(None, self.D_INSTANCE_NAME, self.D_ATTR_NAME)
        else:
            super().__init__(None, self.F_INSTANCE_NAME, self.F_ATTR_NAME)

    def _run_obj_attr(self):
        self._obj_attr()(self._remove_path)
