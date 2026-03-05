"""SubModuleParameter 基底クラスのテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.abc.sub_module_parameter import SubModuleParameter
from jetline.module.sub_module_parameter.value.must_value import MustValue
from jetline.module.sub_module_parameter.value.option_value import OptionValue
from test.abc.base_test_case import BaseTestCase

MEMBER_A = "member_a is member_a"
MEMBER_B = "member_b is member_b"


class ASubModuleParameter(SubModuleParameter):
    """テスト用のサブモジュールパラメータ実装。."""

    def __init__(self, params: dict):
        """入力パラメータを保持して初期化する。.

        Args:
            params: 初期化対象の辞書。
        """
        self._member_a = None
        self._member_b = None
        super().__init__(params)

    @property
    def member_a(self):
        """必須パラメータを返す。."""
        return self._member_a

    @member_a.setter
    def member_a(self, value):
        """必須パラメータを設定する。.

        Args:
            value: 設定値。
        """
        self._member_a = MustValue(value, display=MEMBER_A)

    @property
    def member_b(self):
        """任意パラメータを返す。."""
        return self._member_b

    @member_b.setter
    def member_b(self, value):
        """任意パラメータを設定する。.

        Args:
            value: 設定値。
        """
        self._member_b = OptionValue(value, display=MEMBER_B)


class TestSubModuleParameter(BaseTestCase):
    """SubModuleParameter の共通挙動を確認するテスト。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """必須・任意の両方を指定した場合の読込結果を確認する。."""
        params = {"member_a": "1", "member_b": "2"}
        parameter = ASubModuleParameter(params)

        self.assertEqual("1", parameter.member_a.get())
        self.assertEqual("2", parameter.member_b.get())
        self.assertEqual(MEMBER_A, parameter.member_a.display)
        self.assertEqual(MEMBER_B, parameter.member_b.display)

    def test_must_parameter_not_set(self):
        """必須値が欠けた場合に例外となることを確認する。."""
        params = {"member_b": "2"}

        with self.assertRaises(SubModuleParameterError):
            ASubModuleParameter(params)

    def test_must_parameter(self):
        """必須値のみ指定した場合に任意値が未設定となることを確認する。."""
        params = {"member_a": "1"}
        parameter = ASubModuleParameter(params)

        self.assertEqual("1", parameter.member_a.get())
        self.assertIsNone(parameter.member_b.get())
        self.assertEqual(MEMBER_A, parameter.member_a.display)
        self.assertEqual(MEMBER_B, parameter.member_b.display)

    def test_mix_in_parameter(self):
        """未定義キーが属性として混入しないことを確認する。."""
        params = {
            "member_a": "1",
            "member_b": "2",
            "member_c": {"member_c_1": "c_1", "member_c_2": "c_2"},
        }
        parameter = ASubModuleParameter(params)

        self.assertEqual("1", parameter.member_a.get())
        self.assertEqual("2", parameter.member_b.get())
        with self.assertRaises(AttributeError):
            _ = parameter._member_c
