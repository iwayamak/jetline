"""SubModuleResult のユニットテスト。."""

from jetline.module.sub_module.result.sub_module_result import SubModuleResult
from test.abc.base_test_case import BaseTestCase


class TestSubModuleResult(BaseTestCase):
    """SubModuleResult のログ参照挙動を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._result: SubModuleResult | None = None
        super().__init__(*args, **kwargs)

    def setUp(self):
        """各テスト前に結果コンテナを初期化する。."""
        self._result = SubModuleResult()

    def test_get_last_log_no_data(self):
        """ログ未登録時に各 getter が None を返すことを確認する。."""
        self.assertIsNone(self._result.get_last_log_sub_module_name())
        self.assertIsNone(self._result.get_last_log_processing_time())
        self.assertIsNone(self._result.get_last_log_status())
        self.assertIsNone(self._result.get_last_log_start_time())
        self.assertIsNone(self._result.get_last_log_end_time())
        self.assertIsNone(self._result.get_last_log_data_file())
        self.assertIsNone(self._result.get_last_log_local_data_file_list())
        self.assertIsNone(self._result.get_last_log_s3_data_file_list())

    def test_get_last_log_no_data_file_list(self):
        """ファイル一覧未指定時に空配列として保持されることを確認する。."""
        self._result.append_result(
            "test_sub_module1",
            "2015-02-06 15:12:25,123",
            "2015-02-06 15:12:26,123",
            1.0,
        )

        self.assertEqual("test_sub_module1", self._result.get_last_log_sub_module_name())
        self.assertEqual(1.0, self._result.get_last_log_processing_time())
        self.assertEqual("success", self._result.get_last_log_status())
        self.assertEqual("2015-02-06 15:12:25,123", self._result.get_last_log_start_time())
        self.assertEqual("2015-02-06 15:12:26,123", self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual(0, len(self._result.get_last_log_local_data_file_list()))
        self.assertEqual(0, len(self._result.get_last_log_s3_data_file_list()))

    def test_get_last_log_exists_single_data_file_list(self):
        """単一ファイル結果が正しく保持されることを確認する。."""
        self._result.append_result(
            "test_sub_module2",
            "2015-02-06 16:12:25,123",
            "2015-02-06 16:12:26,123",
            2.0,
            status="error",
            local_data_file_list=["test1.txt"],
            s3_data_file_list=["test2.txt"],
        )

        self.assertEqual("test_sub_module2", self._result.get_last_log_sub_module_name())
        self.assertEqual(2.0, self._result.get_last_log_processing_time())
        self.assertEqual("error", self._result.get_last_log_status())
        self.assertEqual("2015-02-06 16:12:25,123", self._result.get_last_log_start_time())
        self.assertEqual("2015-02-06 16:12:26,123", self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual("test1.txt", self._result.get_last_log_local_data_file_list()[0])
        self.assertEqual("test2.txt", self._result.get_last_log_s3_data_file_list()[0])

    def test_get_last_log_exists_multiple_data_file_list(self):
        """複数ファイル結果が正しく保持されることを確認する。."""
        self._result.append_result(
            "test_sub_module3",
            "2015-02-06 17:12:25,123",
            "2015-02-06 17:12:26,123",
            3.0,
            status="success",
            local_data_file_list=["test21.txt", "test22.txt"],
            s3_data_file_list=["test31.txt", "test32.txt"],
        )

        self.assertEqual("test_sub_module3", self._result.get_last_log_sub_module_name())
        self.assertEqual(3.0, self._result.get_last_log_processing_time())
        self.assertEqual("success", self._result.get_last_log_status())
        self.assertEqual("2015-02-06 17:12:25,123", self._result.get_last_log_start_time())
        self.assertEqual("2015-02-06 17:12:26,123", self._result.get_last_log_end_time())
        self.assertEqual(2, len(self._result.get_last_log_data_file()))
        self.assertEqual("test21.txt", self._result.get_last_log_local_data_file_list()[0])
        self.assertEqual("test22.txt", self._result.get_last_log_local_data_file_list()[1])
        self.assertEqual("test31.txt", self._result.get_last_log_s3_data_file_list()[0])
        self.assertEqual("test32.txt", self._result.get_last_log_s3_data_file_list()[1])

    def test_set_creator_metrics(self):
        """SubModuleCreator メトリクスが metadata へ保持されることを確認する。."""
        metrics = {
            "lazy_hit": 3,
            "lazy_miss": 1,
            "full_scan_parameter": 0,
            "full_scan_sub_module": 0,
        }
        self._result.set_creator_metrics(metrics)
        result_dict = self._result.as_dict()

        self.assertIn(SubModuleResult.KEY_METADATA, result_dict)
        metadata = result_dict[SubModuleResult.KEY_METADATA]
        self.assertEqual(
            metrics,
            metadata[SubModuleResult.KEY_CREATOR_METRICS],
        )

    def test_set_execution_context(self):
        """実行コンテキストが metadata へ保持されることを確認する。."""
        execution_context = {
            "exec_yaml_path": "/tmp/job.yaml",
            "exec_date": "20260305",
            "dry_run_mode": False,
            "tries_count": 2,
            "retry_options": {
                "tries": 3,
                "delay": 1,
                "backoff": 2,
                "jitter": [1, 3],
                "max_delay": 10,
            },
        }
        self._result.set_execution_context(execution_context)
        result_dict = self._result.as_dict()

        self.assertIn(SubModuleResult.KEY_METADATA, result_dict)
        metadata = result_dict[SubModuleResult.KEY_METADATA]
        self.assertEqual(
            execution_context,
            metadata[SubModuleResult.KEY_EXECUTION_CONTEXT],
        )

    def test_set_command_metrics(self):
        """Command メトリクスが metadata へ保持されることを確認する。"""
        command_metrics = {
            "total": 3,
            "succeeded": 2,
            "failed": 1,
            "by_name": {"CopyCommand": {"executed": 2}},
            "by_sub_module": {"LocalProcessingCopy": {"total": 2}},
            "failures": [{"command_name": "RemoveCommand"}],
        }
        self._result.set_command_metrics(command_metrics)
        result_dict = self._result.as_dict()

        self.assertIn(SubModuleResult.KEY_METADATA, result_dict)
        metadata = result_dict[SubModuleResult.KEY_METADATA]
        self.assertEqual(
            command_metrics,
            metadata[SubModuleResult.KEY_COMMAND_METRICS],
        )

    def test_build_sub_module_summary(self):
        """SubModule 単位サマリーが期待どおり生成されることを確認する。"""
        command_metrics = {
            "by_sub_module": {
                "LocalProcessingCopy": {
                    "total": 2,
                    "succeeded": 1,
                    "failed": 1,
                    "by_name": {
                        "CopyCommand": {
                            "executed": 2,
                            "succeeded": 1,
                            "failed": 1,
                            "elapsed_seconds_total": 0.1234,
                        }
                    },
                }
            }
        }
        summary = SubModuleResult.build_sub_module_summary(command_metrics)

        self.assertIn("LocalProcessingCopy", summary)
        local_summary = summary["LocalProcessingCopy"]
        self.assertEqual(2, local_summary["total"])
        self.assertEqual(1, local_summary["succeeded"])
        self.assertEqual(1, local_summary["failed"])
        self.assertEqual(50.0, local_summary["success_rate"])
        self.assertEqual(["CopyCommand"], local_summary["failed_commands"])
        self.assertEqual(0.1234, local_summary["elapsed_seconds_total"])
