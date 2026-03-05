"""LocalProcessingRemoveParameter のユニットテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.local.local_processing_remove_parameter import (
    LocalProcessingRemoveParameter,
)
from test.abc.base_test_case import BaseTestCase


class TestLocalProcessingRemoveParameter(BaseTestCase):
    """ローカル削除用パラメータの検証テスト。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """全パラメータ指定時に値が保持されることを確認する。."""
        param = LocalProcessingRemoveParameter(
            {
                "path_list": ["./test_target_01.csv", "./test_target_02.csv"],
                "use_last_result": True,
            }
        )

        self.assertEqual(["./test_target_01.csv", "./test_target_02.csv"], param.path_list.get())
        self.assertTrue(param.use_last_result.get())

    def test_must_parameter(self):
        """必須パラメータのみでも初期化できることを確認する。."""
        param = LocalProcessingRemoveParameter(
            {"path_list": ["./test_target_01.csv", "./test_target_02.csv"]}
        )

        self.assertEqual(["./test_target_01.csv", "./test_target_02.csv"], param.path_list.get())
        self.assertFalse(param.use_last_result.get())

    def test_path_list_not_list(self):
        """path_list がリストでない場合に例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingRemoveParameter(
                {
                    "path_list": {
                        "target_01": "./test_target_01.csv",
                        "target_02": "./test_target_02.csv",
                    }
                }
            )
