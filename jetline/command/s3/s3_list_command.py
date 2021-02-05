# -*- coding: utf-8 -*-

from .abc.s3_command import S3Command
from ...container.component.s3_component import S3Component


class S3ListCommand(S3Command):

    def __init__(self,
                 component: S3Component,
                 prefix: str,
                 object_list: list):
        self._prefix = prefix
        self._object_list = object_list
        super().__init__(component)

    def run(self):
        super().run()
        summary_iter = self._bucket.objects.filter(Prefix=self._prefix)
        for k in summary_iter:
            self._object_list.append(k)
