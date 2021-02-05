# -*- coding: utf-8 -*-

import os
import glob
import logging
from ..abc.sub_module import SubModule
from ...sub_module_parameter.local.local_processing_remove_parameter import LocalProcessingRemoveParameter
from ....command.command_queue import CommandQueue
from ....command.local.remove_command import RemoveCommand
from ....share_parameter.share_parameter import ShareParameter

logger = logging.getLogger('jetline')


class LocalProcessingRemove(SubModule):

    def __init__(self, param: LocalProcessingRemoveParameter):
        super().__init__(param)

    def run(self):
        path_pattern_list = self._parameter.path_list.get()
        if self._parameter.use_last_result.get():
            path_pattern_list = \
                ShareParameter.sub_module_result.get_last_log_local_data_file_list()
        queue = CommandQueue()
        for path_pattern in path_pattern_list:
            for path in glob.glob(path_pattern):
                if os.path.exists(path):
                    queue.add_command(
                        RemoveCommand(path)
                    )
        queue.execute()
