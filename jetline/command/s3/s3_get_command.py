# -*- coding: utf-8 -*-

from .abc.s3_command import S3Command
from ...container.component.s3_component import S3Component


class S3GetCommand(S3Command):

    def __init__(self,
                 component: S3Component,
                 key: str,
                 file_path: str):
        self._key = key
        self._file_path = file_path
        super().__init__(component)

    def run(self):
        super().run()
        self._bucket.download_file(self._key, self._file_path)
