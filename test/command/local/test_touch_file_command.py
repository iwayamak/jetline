# -*- coding: utf-8 -*-

import os
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase

TEST_DATA_PATH = \
    os.path.join(
        os.path.dirname(__file__),
        'test_touch_file_command.txt'
    )


class TestTouchFileCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(TEST_DATA_PATH)

    def test_touch_file(self):
        ShareParameter.dry_run_mode = False
        if os.path.exists(TEST_DATA_PATH):
            os.remove(TEST_DATA_PATH)
        command = TouchFileCommand(TEST_DATA_PATH)
        command.execute()
        self.assertTrue(os.path.exists(TEST_DATA_PATH))
