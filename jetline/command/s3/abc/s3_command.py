# -*- coding: utf-8 -*-

import logging
import boto3
from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class S3Command(Command):

    def __init__(self, component: Component):
        self._bucket = None
        self._session = None
        self._connection = None
        super().__init__(component)

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        super().run()
        s3 = boto3.resource('s3')
        self._bucket = s3.Bucket(self.component.bucket)

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
