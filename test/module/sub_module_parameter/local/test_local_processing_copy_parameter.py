"""LocalProcessingCopyParameter のユニットテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.local.local_processing_copy_parameter import (
    LocalProcessingCopyParameter,
)
from test.abc.base_test_case import BaseTestCase


class TestLocalProcessingCopyParameter(BaseTestCase):
    """ローカルコピー用パラメータの検証テスト。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """全パラメータ指定時に値が保持されることを確認する。."""
        param = LocalProcessingCopyParameter(
            {"source_path": "./test_source.csv", "destination_path": "./test_destination.csv"}
        )

        self.assertEqual("./test_source.csv", param.source_path.get())
        self.assertEqual("./test_destination.csv", param.destination_path.get())

    def test_source_path_not_set(self):
        """コピー元未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingCopyParameter({"destination_path": "./test_destination.csv"})

    def test_destination_path_not_set(self):
        """コピー先未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            LocalProcessingCopyParameter({"source_path": "./test_source.csv"})
