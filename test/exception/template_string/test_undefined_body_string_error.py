"""UndefinedBodyStringError のユニットテスト。."""

from jetline.exception.template_string.undefined_body_string_error import (
    UndefinedBodyStringError,
)
from test.abc.base_test_case import BaseTestCase


class TestUndefinedBodyStringError(BaseTestCase):
    """UndefinedBodyStringError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """UndefinedBodyStringError が送出できることを確認する。."""
        with self.assertRaises(UndefinedBodyStringError):
            raise UndefinedBodyStringError("undefined body string error")
