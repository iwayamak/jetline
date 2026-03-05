"""BodyStringError のユニットテスト。."""

from jetline.exception.template_string.body_string_error import BodyStringError
from test.abc.base_test_case import BaseTestCase


class TestBodyStringError(BaseTestCase):
    """BodyStringError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """BodyStringError が送出できることを確認する。."""
        with self.assertRaises(BodyStringError):
            raise BodyStringError("body string error")
