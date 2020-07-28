# -*- coding: utf-8 -*-

import logging
from .abc.scp_command import ScpCommand
from ...container.component.scp_component import ScpComponent

logger = logging.getLogger('jetline')


class ScpGetCommand(ScpCommand):

    def __init__(self,
                 component: ScpComponent,
                 remote_path: str,
                 local_dir_path: str,
                 recursive: bool,
                 preserve_times: bool,
                 object_list: list
                 ):
        self._remote_path = remote_path
        self._local_dir_path = local_dir_path
        self._recursive = recursive
        self._preserve_times = preserve_times
        self._object_list = object_list
        super().__init__(component)

    def run(self):
        super().run()
        self.scp.get(
            remote_path=self._remote_path,
            local_path=self._local_dir_path,
            recursive=self._recursive,
            preserve_times=self._preserve_times
        )
        stdout = self.ssh.exec_command(f'ls {self._remote_path}')[1]
        self._object_list = [remote_path.rstrip() for remote_path in stdout]
        logger.info(f'Get {self._object_list} using SCP from {self.component.host}')
