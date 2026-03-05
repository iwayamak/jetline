"""SubModule 基底クラスのユニットテスト。."""

from jetline.module.sub_module.abc.sub_module import SubModule
from jetline.module.sub_module.result.sub_module_result import SubModuleResult
from jetline.module.sub_module_parameter.abc.sub_module_parameter import SubModuleParameter
from jetline.module.sub_module_parameter.value.option_value import OptionValue
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase


class ChildSubModuleParameter(SubModuleParameter):
    """SubModule テスト用パラメータ。."""

    def __init__(self, params: dict | None):
        """テストパラメータを初期化する。."""
        self._member_a = None
        self._member_b = None
        super().__init__(params)

    @property
    def member_a(self):
        """member_a を返す。."""
        return self._member_a.get()

    @property
    def member_b(self):
        """member_b を返す。."""
        return self._member_b.get()

    @member_a.setter
    def member_a(self, value):
        """member_a を設定する。."""
        self._member_a = OptionValue(value)

    @member_b.setter
    def member_b(self, value):
        """member_b を設定する。."""
        self._member_b = OptionValue(value)


class ChildSubModule(SubModule):
    """SubModule テスト用実装。."""

    def __init__(self, param):
        """テスト対象サブモジュールを初期化する。."""
        super().__init__(param)

    def run(self):
        """テストでは実処理を行わない。."""


class ContextAwareChildSubModule(SubModule):
    """実行中のサブモジュール名を検証するテスト用実装。"""

    def __init__(self, param):
        """テスト対象サブモジュールを初期化する。"""
        self.current_name_during_run = None
        super().__init__(param)

    def run(self):
        """実行中の current_sub_module_name を保持する。"""
        self.current_name_during_run = ShareParameter.current_sub_module_name


class TestSubModule(BaseTestCase):
    """SubModule 共通挙動を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def setUp(self):
        """実行結果共有領域を初期化する。."""
        ShareParameter.sub_module_result = SubModuleResult()

    def test_simple(self):
        """通常実行時にパラメータが保持されることを確認する。."""
        parameter = ChildSubModuleParameter({"member_a": "1", "member_b": "2"})
        sub_module = ChildSubModule(parameter)

        self.assertEqual("1", sub_module._parameter.member_a)
        self.assertEqual("2", sub_module._parameter.member_b)
        sub_module.execute()

    def test_none_param(self):
        """None パラメータ初期化時に任意値が None となることを確認する。."""
        parameter = ChildSubModuleParameter(None)
        self.assertIsNone(parameter.member_b)

    def test_normalize_non_empty_paths(self):
        """空文字や None を除外できることを確認する。"""
        parameter = ChildSubModuleParameter({"member_a": "1", "member_b": "2"})
        sub_module = ChildSubModule(parameter)
        self.assertEqual(
            ["a.csv", "b.csv"],
            sub_module.normalize_non_empty_paths(["a.csv", "", None, "b.csv"]),
        )

    def test_expand_glob_patterns(self):
        """Glob 展開とリテラル保持を同時に行えることを確認する。"""
        parameter = ChildSubModuleParameter({"member_a": "1", "member_b": "2"})
        sub_module = ChildSubModule(parameter)
        expanded = sub_module.expand_glob_patterns(
            [
                "test/module/sub_module/abc/test_sub_module.py",
                "test/module/sub_module/abc/*.py",
            ]
        )
        self.assertIn("test/module/sub_module/abc/test_sub_module.py", expanded)
        self.assertIn("test/module/sub_module/abc/__init__.py", expanded)

    def test_get_last_result_local_paths_without_log(self):
        """ログ未登録時に空配列を返すことを確認する。"""
        parameter = ChildSubModuleParameter({"member_a": "1", "member_b": "2"})
        sub_module = ChildSubModule(parameter)
        self.assertEqual([], sub_module.get_last_result_local_paths())

    def test_execute_sets_and_restores_current_sub_module_name(self):
        """実行中にサブモジュール名が設定され、終了後に復元されることを確認する。"""
        ShareParameter.current_sub_module_name = "BeforeSubModule"
        parameter = ChildSubModuleParameter({"member_a": "1", "member_b": "2"})
        sub_module = ContextAwareChildSubModule(parameter)

        sub_module.execute()

        self.assertEqual("ContextAwareChildSubModule", sub_module.current_name_during_run)
        self.assertEqual("BeforeSubModule", ShareParameter.current_sub_module_name)
