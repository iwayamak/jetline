# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.command.s3.s3_list_command import S3ListCommand
from jetline.command.s3.s3_put_command import S3PutCommand
from jetline.container.container import Container

TEST_DATA_PATH_LIST = [
    os.path.join(
            os.path.dirname(__file__),
            f'test_s3_list_command_0{i}.csv'
    )
    for i in range(2)
]


class TestS3ListCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = \
            Container().component('S3_COMPONENT.ID=UT')
        self._test_data_path = \
            os.path.join(
                os.path.dirname(__file__), 'test_data'
            )
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        queue = CommandQueue()
        for test_data_path in TEST_DATA_PATH_LIST:
            queue.add_command(
                TouchFileCommand(test_data_path)
            )
            queue.add_command(
                S3PutCommand(
                    Container().component('S3_COMPONENT.ID=UT'),
                    test_data_path,
                    f'test_s3_list_command/{os.path.basename(test_data_path)}'
                )
            )
        queue.execute()

    def test_s3_list(self):
        prefix = 'test_s3_list_command'
        object_list = []
        command = \
            S3ListCommand(
                self._component, prefix, object_list
            )
        command.execute()
        for i, test_data_path in enumerate(TEST_DATA_PATH_LIST):
            self.assertEqual(
                object_list[i].key,
                f'test_s3_list_command/{os.path.basename(test_data_path)}'
            )
        self.assertEqual(len(object_list), len(TEST_DATA_PATH_LIST))
