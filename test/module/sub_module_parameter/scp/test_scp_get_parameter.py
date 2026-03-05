"""ScpGetParameter のユニットテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.scp.scp_get_parameter import ScpGetParameter
from test.abc.base_test_case import BaseTestCase


class TestScpGetParameter(BaseTestCase):
    """SCP ダウンロード用パラメータの検証テスト。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """全パラメータ指定時に値が保持されることを確認する。."""
        param = ScpGetParameter(
            {
                "scp_component_key": "SCP_COMPONENT.ID=UT",
                "remote_path": "/tmp/remote/*",
                "local_dir_path": "/tmp/local",
                "recursive": True,
                "preserve_times": True,
            }
        )

        self.assertEqual("SCP_COMPONENT.ID=UT", param.scp_component_key.get())
        self.assertEqual("/tmp/remote/*", param.remote_path.get())
        self.assertEqual("/tmp/local", param.local_dir_path.get())
        self.assertTrue(param.recursive.get())
        self.assertTrue(param.preserve_times.get())

    def test_must_parameter(self):
        """必須パラメータのみでも初期化できることを確認する。."""
        param = ScpGetParameter(
            {
                "scp_component_key": "SCP_COMPONENT.ID=UT",
                "remote_path": "/tmp/remote/*",
                "local_dir_path": "/tmp/local",
            }
        )

        self.assertEqual("SCP_COMPONENT.ID=UT", param.scp_component_key.get())
        self.assertEqual("/tmp/remote/*", param.remote_path.get())
        self.assertEqual("/tmp/local", param.local_dir_path.get())
        self.assertFalse(param.recursive.get())
        self.assertFalse(param.preserve_times.get())

    def test_component_key_not_set(self):
        """コンポーネントキー未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter({"remote_path": "/tmp/remote/*", "local_dir_path": "/tmp/local"})

    def test_remote_path_not_set(self):
        """リモートパス未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {"scp_component_key": "SCP_COMPONENT.ID=UT", "local_dir_path": "/tmp/local"}
            )

    def test_local_dir_path_not_set(self):
        """ローカル保存先未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {"scp_component_key": "SCP_COMPONENT.ID=UT", "remote_path": "/tmp/remote/*"}
            )

    def test_recursive_not_bool(self):
        """Recursive が真偽値でない場合に例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    "scp_component_key": "SCP_COMPONENT.ID=UT",
                    "remote_path": "/tmp/remote/*",
                    "local_dir_path": "/tmp/local",
                    "recursive": "not recursive",
                }
            )

    def test_preserve_times_not_bool(self):
        """preserve_times が真偽値でない場合に例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            ScpGetParameter(
                {
                    "scp_component_key": "SCP_COMPONENT.ID=UT",
                    "remote_path": "/tmp/remote/*",
                    "local_dir_path": "/tmp/local",
                    "preserve_times": "none preserve_times",
                }
            )
