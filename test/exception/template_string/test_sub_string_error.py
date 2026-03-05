"""TemplateStringError のユニットテスト。."""

from jetline.exception.template_string.sub_string_error import TemplateStringError
from test.abc.base_test_case import BaseTestCase


class TestTemplateStringError(BaseTestCase):
    """TemplateStringError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """TemplateStringError が送出できることを確認する。."""
        with self.assertRaises(TemplateStringError):
            raise TemplateStringError("template string error")
