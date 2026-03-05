"""Module メタデータ構築のユニットテスト。"""

import os

from jetline.module.module import Module
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase


class TestModuleMetadata(BaseTestCase):
    """結果メタデータへ実行情報が含まれることを検証する。"""

    def test_build_execution_context_metadata_includes_command_metrics(self):
        """実行コンテキストに command_metrics が含まれることを確認する。"""
        exec_yaml_path = os.path.join(
            os.path.dirname(__file__),
            "sample_yaml",
            "local",
            "test_local_processing_copy.yaml",
        )
        module = Module(exec_yaml_path, "20260305")
        ShareParameter.command_metrics = {
            "total": 3,
            "succeeded": 2,
            "failed": 1,
            "by_name": {"CopyCommand": {"executed": 2}},
            "by_sub_module": {"LocalProcessingCopy": {"total": 2}},
            "failures": [{"command_name": "RemoveCommand"}],
        }

        metadata = module._build_execution_context_metadata()

        self.assertIn("command_metrics", metadata)
        self.assertEqual(3, metadata["command_metrics"]["total"])
        self.assertEqual(1, metadata["command_metrics"]["failed"])
