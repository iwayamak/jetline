# -*- coding: utf-8 -*-

import logging
from ..abc.sub_module import SubModule
from ...sub_module_parameter.local.local_processing_copy_parameter import LocalProcessingCopyParameter
from ....command.local.copy_command import CopyCommand

logger = logging.getLogger('jetline')


class LocalProcessingCopy(SubModule):

    def __init__(self, param: LocalProcessingCopyParameter):
        super().__init__(param)

    def run(self):
        command = CopyCommand(
            self._parameter.source_path.get(),
            self._parameter.destination_path.get()
        )
        command.execute()
