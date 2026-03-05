"""PlaceHolder のユニットテスト。."""

import os

from jetline.share_parameter.share_parameter import ShareParameter
from jetline.substr.place_holder import PlaceHolder
from test.abc.base_test_case import BaseTestCase


class TestPlaceHolder(BaseTestCase):
    """PlaceHolder のテンプレート展開を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_exec(self):
        """テンプレート変数が正しく置換されることを確認する。."""
        ShareParameter.exec_date = "20200401"
        filename = os.path.join(os.path.dirname(__file__), "test_place_holder.txt")
        correct_result = "20200401 hello good-bye"
        template = PlaceHolder(
            filename,
            {
                "elem_1": "hello",
                "elem_2": "good-bye",
                "elem_3": "see you",
            },
        )
        result = template.apply()
        self.assertEqual(correct_result, result)
