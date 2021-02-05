# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.command.local.remove_command import RemoveCommand
from jetline.command.s3.s3_get_command import S3GetCommand
from jetline.command.s3.s3_put_command import S3PutCommand
from jetline.container.container import Container

PREPARE_TEST_DATA_PATH = \
    os.path.join(
        os.path.dirname(__file__),
        'test_s3_get_command.csv'
    )

TEST_DATA_PATH = \
    os.path.join(
        os.path.dirname(__file__),
        'test_data',
        'test_s3_get_command.tsv'
    )


class TestS3GetCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = \
            Container().component('S3_COMPONENT.ID=UT')
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        queue = CommandQueue()
        queue.add_command(
            TouchFileCommand(PREPARE_TEST_DATA_PATH)
        )
        queue.add_command(
            S3PutCommand(
                Container().component('S3_COMPONENT.ID=UT'),
                PREPARE_TEST_DATA_PATH,
                os.path.basename(PREPARE_TEST_DATA_PATH)
            )
        )
        queue.execute()

    @classmethod
    def tearDownClass(cls) -> None:
        queue = CommandQueue()
        queue.add_command(
            RemoveCommand(PREPARE_TEST_DATA_PATH)
        )
        queue.add_command(
            RemoveCommand(TEST_DATA_PATH)
        )
        queue.execute()

    def test_s3_get(self):
        key = 'test_s3_get_command.csv'
        command = \
            S3GetCommand(
                self._component, key, TEST_DATA_PATH
            )
        command.execute()
