# -*- coding: utf-8 -*-

import os
from ...abc.base_test_case import BaseTestCase
from jetline.command.command_queue import CommandQueue
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.command.local.remove_command import RemoveCommand
from jetline.command.scp.scp_get_command import ScpGetCommand
from jetline.command.scp.scp_put_command import ScpPutCommand
from jetline.container.container import Container

TEST_DATA_PATH_LIST = \
   [
       os.path.join(os.path.dirname(__file__), f'test_scp_get_command_0{i}.csv') for i in range(5)
    ]

REMOTE_DIR = '/tmp'


class TestScpGetCommand(BaseTestCase):

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
        queue.add_command(
            ScpPutCommand(
                Container().component('SCP_COMPONENT.ID=UT'),
                TEST_DATA_PATH_LIST,
                REMOTE_DIR,
                False,
                False
            )
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

    def test_scp_get_single(self):
        object_list = []
        command = \
            ScpGetCommand(
                self._component,
                os.path.join(REMOTE_DIR, 'test_scp_get_command_00.csv'),
                os.path.dirname(__file__),
                False,
                False,
                object_list
            )
        command.execute()

    def test_scp_get_multiple(self):
        object_list = []
        command = \
            ScpGetCommand(
                self._component,
                os.path.join(REMOTE_DIR, 'test_scp_get_command_0*.csv'),
                os.path.dirname(__file__),
                False,
                False,
                object_list
            )
        command.execute()
