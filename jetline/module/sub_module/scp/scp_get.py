# -*- coding: utf-8 -*-

import os
from ..abc.sub_module import SubModule
from ...sub_module_parameter.scp.scp_get_parameter import ScpGetParameter
from ....command.scp.scp_get_command import ScpGetCommand
from ....util.path_util import PathUtil
from ....container.container import Container


class ScpGet(SubModule):

    def __init__(self, param: ScpGetParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.scp_component_key.get()
            )
        object_list = []
        PathUtil.mkdir_if_not_exists(self._parameter.local_dir_path.get())
        command = \
            ScpGetCommand(
                component,
                self._parameter.remote_path.get(),
                self._parameter.local_dir_path.get(),
                self._parameter.recursive.get(),
                self._parameter.preserve_times.get(),
                object_list
            )
        command.execute()
        self._result_local_file_list = [object_list]
