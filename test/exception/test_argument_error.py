"""ArgumentError のユニットテスト。."""

from jetline.exception.argument_error import ArgumentError
from test.abc.base_test_case import BaseTestCase


class TestArgumentError(BaseTestCase):
    """ArgumentError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """ArgumentError が送出できることを確認する。."""
        with self.assertRaises(ArgumentError):
            raise ArgumentError("argument error")
