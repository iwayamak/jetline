# -*- coding: utf-8 -*-

from .abc.s3_command import S3Command
from ...container.component.s3_component import S3Component


class S3PutCommand(S3Command):

    def __init__(self,
                 component: S3Component,
                 file_path: str,
                 key: str):
        self._file_path = file_path
        self._key = key
        super().__init__(component)

    def run(self):
        super().run()
        self._bucket.upload_file(self._file_path, self._key)
