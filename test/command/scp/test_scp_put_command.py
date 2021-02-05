# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.command.local.remove_command import RemoveCommand
from jetline.command.scp.scp_put_command import ScpPutCommand
from jetline.container.container import Container

TEST_DATA_PATH_LIST = \
   [
       os.path.join(os.path.dirname(__file__), f'test_scp_put_command_0{i}.csv') for i in range(5)
    ]

REMOTE_DIR = '/tmp'


class TestScpPutCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        self._component = \
            Container().component('SCP_COMPONENT.ID=UT')
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        queue = CommandQueue()
        for test_data_path in TEST_DATA_PATH_LIST:
            queue.add_command(
                TouchFileCommand(test_data_path)
            )
        queue.execute()

    @classmethod
    def tearDownClass(cls) -> None:
        queue = CommandQueue()
        for test_data_path in TEST_DATA_PATH_LIST:
            queue.add_command(
                RemoveCommand(test_data_path)
            )
        queue.execute()

    def test_scp_put_single(self):
        command = \
            ScpPutCommand(
                self._component,
                [TEST_DATA_PATH_LIST[0]],
                REMOTE_DIR,
                False,
                False
            )
        command.execute()

    def test_scp_put_multiple(self):
        command = \
            ScpPutCommand(
                self._component,
                TEST_DATA_PATH_LIST,
                REMOTE_DIR,
                False,
                False
            )
        command.execute()
