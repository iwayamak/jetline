# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from ....command.s3.s3_put_command import S3PutCommand
from ....container.container import Container


class TestS3PutCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = \
            Container().component('S3_COMPONENT.ID=UT')
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), 'test_data'
            )
        super().__init__(*args, **kwargs)

    def test_s3_put(self):
        file_name = \
            os.path.join(
                self._test_data_path,
                'test_s3_put_command.tsv'
            )
        key = os.path.basename(file_name)
        command = S3PutCommand(
            self._component,
            file_name,
            key
        )
        command.execute()
