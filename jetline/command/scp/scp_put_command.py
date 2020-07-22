# -*- coding: utf-8 -*-

import logging
from .abc.scp_command import ScpCommand
from ...container.component.scp_component import ScpComponent

logger = logging.getLogger('jetline')


class ScpPutCommand(ScpCommand):

    def __init__(self,
                 component: ScpComponent,
                 local_path_list: list,
                 remote_dir_path: str,
                 recursive: bool,
                 preserve_times: bool,
                 ):
        self._local_path_list = local_path_list
        self._remote_dir_path = remote_dir_path
        self._recursive = recursive
        self._preserve_times = preserve_times
        super().__init__(component)

    def run(self):
        super().run()
        self.scp.put(
            files=self._local_path_list,
            remote_path=self._remote_dir_path,
            recursive=self._recursive,
            preserve_times=self._preserve_times
        )
        logger.info(f'Put {self._local_path_list} using SCP from {self.component.host}')
