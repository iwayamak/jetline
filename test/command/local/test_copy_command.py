# -*- coding: utf-8 -*-

import os
from jetline.command.local.copy_command import CopyCommand
from jetline.command.local.remove_command import RemoveCommand
from jetline.util.path_util import PathUtil
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase

TEST_DATA_PATH = \
    os.path.join(
        os.path.dirname(__file__), 'test_data'
    )


class TestCopyCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        PathUtil.mkdir_if_not_exists(TEST_DATA_PATH)

    def setUp(self) -> None:
        ShareParameter.dry_run_mode = False

    def test_copy_file(self):
        source_file_path = os.path.join(
            TEST_DATA_PATH,
            'test_copy_command.csv'
        )
        destination_file_path = os.path.join(
            TEST_DATA_PATH,
            'test_copy_command_dest.csv'
        )
        if not os.path.exists(source_file_path):
            with open(source_file_path, 'a'):
                os.uname()
        command = CopyCommand(
            source_file_path, destination_file_path
        )
        command.execute()
        self.assertTrue(os.path.exists(destination_file_path))

    def test_copy_directory(self):
        source_directory_path = os.path.join(
            TEST_DATA_PATH,
            'test_copy_command_directory'
        )
        destination_directory_path = os.path.join(
            TEST_DATA_PATH,
            'test_copy_command_dest_directory'
        )
        PathUtil.mkdir_if_not_exists(source_directory_path)
        command = CopyCommand(
            source_directory_path, destination_directory_path
        )
        command.execute()
        self.assertTrue(os.path.exists(destination_directory_path))

    @classmethod
    def tearDownClass(cls) -> None:
        command = RemoveCommand(TEST_DATA_PATH)
        command.execute()
