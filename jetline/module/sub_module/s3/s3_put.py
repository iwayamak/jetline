# -*- coding: utf-8 -*-

import os
import glob
from ..abc.sub_module import SubModule
from ...sub_module_parameter.s3.s3_put_parameter import S3PutParameter
from ....command.local.touch_file_command import TouchFileCommand
from ....command.s3.s3_put_command import S3PutCommand
from ....command.command_queue import CommandQueue
from ....container.container import Container


class S3Put(SubModule):

    def __init__(self, param: S3PutParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.s3_component_key.get()
            )
        queue = CommandQueue()
        file_path_list = glob.glob(self._parameter.local_file_path.get(), recursive=True)

        # end file
        end_file_name = self._parameter.end_file_name.get()
        if end_file_name is not None:
            queue.add_command(TouchFileCommand(end_file_name))
            file_path_list.append(end_file_name)

        for file_path in file_path_list:
            s3_key = os.path.join(
                self._parameter.s3_dir_path.get(),
                os.path.basename(file_path)
            )
            queue.add_command(
                S3PutCommand(
                    component, file_path, s3_key
                )
            )
        queue.execute()
