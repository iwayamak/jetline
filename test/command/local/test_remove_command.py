"""RemoveCommand のユニットテスト。."""

import os

from jetline.command.local.remove_command import RemoveCommand
from jetline.share_parameter.share_parameter import ShareParameter
from jetline.util.path_util import PathUtil
from test.abc.base_test_case import BaseTestCase


class TestRemoveCommand(BaseTestCase):
    """RemoveCommand の削除処理を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        """Dry-run を無効化する。."""
        ShareParameter.dry_run_mode = False

    def test_remove_file(self):
        """ファイル削除が成功することを確認する。."""
        file_path = os.path.join(os.path.dirname(__file__), "test_remove_command_file")
        if not os.path.exists(file_path):
            with open(file_path, "a", encoding="utf-8"):
                pass

        command = RemoveCommand(file_path)
        command.execute()
        self.assertFalse(os.path.exists(file_path))

    def test_remove_directory(self):
        """ディレクトリ削除が成功することを確認する。."""
        directory_path = os.path.join(os.path.dirname(__file__), "test_remove_command_dir")
        PathUtil.mkdir_if_not_exists(directory_path)
        command = RemoveCommand(directory_path)
        command.execute()
        self.assertFalse(os.path.exists(directory_path))
