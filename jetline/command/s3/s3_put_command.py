# -*- coding: utf-8 -*-

from .abc.s3_command import S3Command


class S3PutCommand(S3Command):

    def __init__(self, component: S3Command, file_name: str, key: str):
        self._file_name = file_name
        self._key = key
        super().__init__(component)

    def run(self):
        super().run()
        self._bucket.upload_file(self._file_name, Key=self._key)
