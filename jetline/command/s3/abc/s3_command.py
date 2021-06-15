# -*- coding: utf-8 -*-

import logging
from boto3.session import Session
from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class S3Command(Command):

    def __init__(self, component: Component):
        self._bucket = None
        super().__init__(component)

    def set_up(self):
        super().set_up()

    def body(self):
        super().body()

    def run(self):
        super().run()
        session = Session(
            aws_access_key_id=self.component.aws_access_key,
            aws_secret_access_key=self.component.aws_secret_access_key,
            region_name=self.component.region_name
        )
        s3 = session.resource('s3')
        self._bucket = s3.Bucket(self.component.bucket)

    def dry_run(self):
        super().dry_run()

    def tear_down(self):
        super().tear_down()
