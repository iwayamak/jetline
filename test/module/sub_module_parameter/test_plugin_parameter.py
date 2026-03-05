"""PluginParameter のユニットテスト。."""

import os

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.plugin_parameter import PluginParameter
from test.abc.base_test_case import BaseTestCase


class TestPluginParameter(BaseTestCase):
    """PluginParameter の入力検証を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._plugin_path = os.path.join(os.path.dirname(__file__), "plugins")
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """全パラメータ指定時に値が保持されることを確認する。."""
        param = PluginParameter(
            {
                "plugin_path": self._plugin_path,
                "package": "sample_command",
                "class_name": "SampleCommand",
                "kwargs": {"key1": "value1"},
            }
        )

        self.assertEqual(self._plugin_path, param.plugin_path.get())
        self.assertEqual("sample_command", param.package.get())
        self.assertEqual("SampleCommand", param.class_name.get())
        self.assertEqual({"key1": "value1"}, param.kwargs.get())

    def test_must_parameter(self):
        """必須パラメータのみで初期化できることを確認する。."""
        param = PluginParameter(
            {
                "plugin_path": self._plugin_path,
                "package": "sample_command",
                "class_name": "SampleCommand",
            }
        )

        self.assertEqual(self._plugin_path, param.plugin_path.get())
        self.assertEqual("sample_command", param.package.get())
        self.assertEqual("SampleCommand", param.class_name.get())

    def test_plugin_path_not_set(self):
        """プラグインパス未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PluginParameter({"package": "sample_command.py", "class_name": "SampleCommand"})

    def test_plugin_path_not_exists(self):
        """存在しないプラグインパス指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PluginParameter(
                {
                    "plugin_path": os.path.join(os.path.dirname(__file__), "plugins2"),
                    "package": "sample_command.py",
                    "class_name": "SampleCommand",
                }
            )

    def test_package_not_set(self):
        """パッケージ未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PluginParameter({"plugin_path": self._plugin_path, "class_name": "SampleCommand"})

    def test_class_name_not_set(self):
        """クラス名未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PluginParameter({"plugin_path": self._plugin_path, "package": "sample_command.py"})

    def test_kwargs_not_dict(self):
        """Kwargs が辞書でない場合に例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PluginParameter({"plugin_path": self._plugin_path, "kwargs": "1"})
