# -*- coding: utf-8 -*-

import glob
from ..abc.sub_module import SubModule
from ...sub_module_parameter.scp.scp_put_parameter import ScpPutParameter
from ....command.scp.scp_put_command import ScpPutCommand
from ....container.container import Container
from ....share_parameter.share_parameter import ShareParameter


class ScpPut(SubModule):

    def __init__(self, param: ScpPutParameter):
        super().__init__(param)

    def run(self):
        local_path_list = glob.glob(self._parameter.local_path.get())
        if self._parameter.use_last_result.get():
            local_path_list = \
                ShareParameter.sub_module_result.get_last_log_local_data_file_list()
        component = \
            Container.component(
                self._parameter.scp_component_key.get()
            )

        command = \
            ScpPutCommand(
                component,
                local_path_list,
                self._parameter.remote_dir_path.get(),
                self._parameter.recursive.get(),
                self._parameter.preserve_times.get(),
            )
        command.execute()
