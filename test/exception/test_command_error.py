"""CommandError のユニットテスト。."""

from jetline.exception.command_error import CommandError
from test.abc.base_test_case import BaseTestCase


class TestCommandError(BaseTestCase):
    """CommandError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """終了コードが整数でも送出できることを確認する。."""
        with self.assertRaises(CommandError):
            raise CommandError(1, "command -c xxx")

    def test_raise_str(self):
        """終了コードが文字列でも送出できることを確認する。."""
        with self.assertRaises(CommandError):
            raise CommandError("error", "command -c xxx")
