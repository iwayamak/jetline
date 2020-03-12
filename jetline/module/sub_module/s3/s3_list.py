# -*- coding: utf-8 -*-

import logging
import fnmatch
import dateutil.tz as tz
from ..abc.sub_module import SubModule
from ...sub_module_parameter.s3.s3_list_parameter import S3ListParameter
from ....command.s3.s3_list_command import S3ListCommand
from ....container.container import Container

logger = logging.getLogger('jetline')


class S3List(SubModule):

    def __init__(self, param: S3ListParameter):
        super().__init__(param)

    def run(self):
        component = \
            Container.component(
                self._parameter.s3_component_key.get()
            )
        prefix = self._parameter.s3_file_path.get().split('*')[0]
        object_list = []
        command = S3ListCommand(
            component, prefix, object_list
        )
        command.execute()
        self._result_s3_file_list = \
            [s3_object for s3_object in object_list
             if fnmatch.fnmatch(s3_object.key, self._parameter.s3_file_path.get())]
        for result_s3_file in self._result_s3_file_list:
            last_modified = \
                result_s3_file.last_modified.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
            size = str(result_s3_file.size).rjust(13)
            logger.info(
                f'{last_modified} {size} Bytes {result_s3_file.key}'
            )
