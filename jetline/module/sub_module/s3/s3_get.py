# -*- coding: utf-8 -*-

import os
import fnmatch
from ..abc.sub_module import SubModule
from ...sub_module_parameter.s3.s3_get_parameter import S3GetParameter
from ....command.local.touch_file_command import TouchFileCommand
from ....command.s3.s3_get_command import S3GetCommand
from ....command.s3.s3_list_command import S3ListCommand
from ....command.command_queue import CommandQueue
from ....container.container import Container


class S3Get(SubModule):

    def __init__(self, param: S3GetParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.s3_component_key.get()
            )
        queue = CommandQueue()
        prefix = self._parameter.s3_file_path.get().split('*')[0]
        object_list = []
        command = S3ListCommand(
            component, prefix, object_list
        )
        command.execute()
        key_list = [s3_object.key for s3_object in object_list]
        file_path_list = fnmatch.filter(key_list, self._parameter.s3_file_path.get())

        for file_path in file_path_list:
            queue.add_command(
                S3GetCommand(
                    component,
                    file_path,
                    os.path.join(
                        self._parameter.local_dir_path.get(),
                        os.path.basename(file_path)
                    )
                )
            )
        # end file
        end_file_name = self._parameter.end_file_name.get()
        if end_file_name is not None:
            queue.add_command(TouchFileCommand(end_file_name))
            file_path_list.append(end_file_name)
        queue.execute()
