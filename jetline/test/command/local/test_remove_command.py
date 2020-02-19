import os
from ....command.local.remove_command import RemoveCommand
from ....share_parameter.share_parameter import ShareParameter
from ....test.abc.base_test_case import BaseTestCase


class TestRemoveCommand(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_execute(self):
        f = os.path.join(os.path.dirname(__file__), 'test_remove_command_file')
        d = os.path.join(os.path.dirname(__file__), 'test_remove_command_dir')
        ShareParameter.dry_run_mode = False

        if not os.path.exists(d):
            os.mkdir(d)

        if not os.path.exists(f):
            with open(f, 'a'):
                os.uname()

        command = RemoveCommand(f)
        command.execute()

        command2 = RemoveCommand(d)
        command2.execute()

        self.assertFalse(os.path.exists(f))
        self.assertFalse(os.path.exists(d))
