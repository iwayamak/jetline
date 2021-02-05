# -*- coding: utf-8 -*-

import os
from jetline.command.local.remove_command import RemoveCommand
from jetline.util.path_util import PathUtil
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase


class TestRemoveCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        ShareParameter.dry_run_mode = False

    def test_remove_file(self):
        file_path = os.path.join(
            os.path.dirname(__file__),
            'test_remove_command_file'
        )
        if not os.path.exists(file_path):
            with open(file_path, 'a'):
                os.uname()
        command = RemoveCommand(file_path)
        command.execute()
        self.assertFalse(os.path.exists(file_path))

    def test_remove_directory(self):
        directory_path = os.path.join(
            os.path.dirname(__file__),
            'test_remove_command_dir'
        )
        PathUtil.mkdir_if_not_exists(directory_path)
        command2 = RemoveCommand(directory_path)
        command2.execute()
        self.assertFalse(os.path.exists(directory_path))
