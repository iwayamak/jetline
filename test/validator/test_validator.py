"""Validator デコレータのユニットテスト."""

import datetime
import os

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.validator.validator import Validator

from ..abc.base_test_case import BaseTestCase


class TestValidator(BaseTestCase):
    """各 Validator デコレータの検証ロジックを確認する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        super().__init__(*args, **kwargs)

    @Validator.path
    def set_path(self, path_value):
        """`Validator.path` の検証対象メソッド.

        Args:
            path_value: 検証対象のパス.
        """

    def test_path(self) -> None:
        """既存パスのみ許容されることを確認する."""
        file_path = os.path.join(os.path.dirname(__file__), "test_validator.tsv")
        not_exist_path = os.path.join(os.path.dirname(__file__), "test_validator2.tsv")
        self.set_path(file_path)
        self.set_path(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_path(not_exist_path)

    @Validator.component_key
    def set_component_key(self, key):
        """`Validator.component_key` の検証対象メソッド.

        Args:
            key: コンポーネントキー.
        """

    def test_component_key(self) -> None:
        """コンポーネントキー形式の妥当性を確認する."""
        self.set_component_key("POSTGRESQL_COMPONENT.ID=UT")
        self.set_component_key(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_component_key("invalid")

    @Validator.digit
    def set_digit(self, value):
        """`Validator.digit` の検証対象メソッド.

        Args:
            value: 数値として評価される値.
        """

    def test_digit(self) -> None:
        """整数文字列/整数のみ許容されることを確認する."""
        self.set_digit(123)
        self.set_digit("123")
        self.set_digit(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_digit("1.1")
        with self.assertRaises(SubModuleParameterError):
            self.set_digit("12a")
        with self.assertRaises(SubModuleParameterError):
            self.set_digit(datetime.datetime.now())

    @Validator.boolean
    def set_boolean(self, value):
        """`Validator.boolean` の検証対象メソッド.

        Args:
            value: 真偽値として評価される値.
        """

    def test_boolean(self) -> None:
        """真偽値表現の許容/拒否パターンを確認する."""
        self.set_boolean(True)
        self.set_boolean(False)
        self.set_boolean("true")
        self.set_boolean("FALSE")
        self.set_boolean("on")
        self.set_boolean("oFF")
        self.set_boolean("1")
        self.set_boolean(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean("abc")
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean("OK")
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(0)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(-1)
        with self.assertRaises(SubModuleParameterError):
            self.set_boolean(datetime.datetime.now())

    @Validator.regexp("^(append|replace|truncate|update)$")
    def set_regexp(self, value):
        """`Validator.regexp` の検証対象メソッド.

        Args:
            value: 正規表現で評価される値.
        """

    def test_regexp(self) -> None:
        """正規表現条件の許容/拒否を確認する."""
        self.set_regexp("append")
        self.set_regexp("replace")
        self.set_regexp("truncate")
        self.set_regexp("update")
        self.set_regexp(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp("app")
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp("appendappend")
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp("ab_replace_c")
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp("delete")
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(111)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(True)

    @Validator.range(-2, 2)
    def set_range(self, value):
        """`Validator.range` の検証対象メソッド.

        Args:
            value: 範囲で評価される値.
        """

    def test_range(self) -> None:
        """範囲条件の許容/拒否を確認する."""
        self.set_range(-2)
        self.set_range(0)
        self.set_range(+1)
        self.set_range(2)
        self.set_range(-1.1)
        self.set_range(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_range("app")
        with self.assertRaises(SubModuleParameterError):
            self.set_range("1")
        with self.assertRaises(SubModuleParameterError):
            self.set_range(-2.1)
        with self.assertRaises(SubModuleParameterError):
            self.set_range(2.1)
        with self.assertRaises(SubModuleParameterError):
            self.set_regexp(False)

    @Validator.list
    def set_list(self, value):
        """`Validator.list` の検証対象メソッド.

        Args:
            value: リストとして評価される値.
        """

    def test_list(self) -> None:
        """リスト型条件の許容/拒否を確認する."""
        self.set_list(["item", "item2"])
        self.set_list([])
        self.set_list(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_list(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_list("list")
        with self.assertRaises(SubModuleParameterError):
            self.set_list(datetime.datetime.now())

    @Validator.dict
    def set_dict(self, value):
        """`Validator.dict` の検証対象メソッド.

        Args:
            value: 辞書として評価される値.
        """

    def test_dict(self) -> None:
        """辞書型条件の許容/拒否を確認する."""
        self.set_dict({"key1": "item", "key2": "item2"})
        self.set_dict({})
        self.set_dict(None)
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(1)
        with self.assertRaises(SubModuleParameterError):
            self.set_dict("dict")
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(datetime.datetime.now())
        with self.assertRaises(SubModuleParameterError):
            self.set_dict(["item", "item2"])
        with self.assertRaises(SubModuleParameterError):
            self.set_dict([])
