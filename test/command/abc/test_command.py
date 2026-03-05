"""Command 基底クラスのユニットテスト。"""

from jetline.command.abc.command import Command
from jetline.share_parameter.share_parameter import ShareParameter
from test.abc.base_test_case import BaseTestCase


class SuccessCommand(Command):
    """成功するテスト用コマンド。"""

    def __init__(self):
        """テスト用コマンドを初期化する。"""
        self.run_called = False
        self.dry_run_called = False
        super().__init__(None)

    def run(self):
        """通常実行時の処理。"""
        self.run_called = True

    def dry_run(self):
        """ドライラン時の処理。"""
        self.dry_run_called = True


class FailureCommand(Command):
    """失敗するテスト用コマンド。"""

    def run(self):
        """通常実行時に例外を送出する。"""
        raise RuntimeError("boom")

    def dry_run(self):
        """ドライラン時の処理。"""
        return None


class TestCommand(BaseTestCase):
    """Command の実行メトリクス更新を検証する。"""

    def setUp(self):
        """各テスト前にコマンドメトリクスを初期化する。"""
        ShareParameter.command_metrics = {
            "total": 0,
            "succeeded": 0,
            "failed": 0,
            "by_name": {},
            "by_sub_module": {},
            "failures": [],
        }
        ShareParameter.current_sub_module_name = None

    def test_execute_success_updates_metrics(self):
        """成功実行時にメトリクスが更新されることを確認する。"""
        ShareParameter.dry_run_mode = False
        command = SuccessCommand()

        command.execute()

        metrics = ShareParameter.command_metrics
        self.assertTrue(command.run_called)
        self.assertFalse(command.dry_run_called)
        self.assertEqual(1, metrics["total"])
        self.assertEqual(1, metrics["succeeded"])
        self.assertEqual(0, metrics["failed"])
        self.assertEqual(1, metrics["by_name"]["SuccessCommand"]["executed"])
        self.assertEqual(1, metrics["by_name"]["SuccessCommand"]["succeeded"])
        self.assertEqual(0, metrics["by_name"]["SuccessCommand"]["failed"])
        self.assertGreaterEqual(
            metrics["by_name"]["SuccessCommand"]["elapsed_seconds_total"],
            0.0,
        )

    def test_execute_dry_run_updates_metrics(self):
        """ドライラン実行時に成功メトリクスが更新されることを確認する。"""
        ShareParameter.dry_run_mode = True
        command = SuccessCommand()

        command.execute()

        metrics = ShareParameter.command_metrics
        self.assertFalse(command.run_called)
        self.assertTrue(command.dry_run_called)
        self.assertEqual(1, metrics["total"])
        self.assertEqual(1, metrics["succeeded"])
        self.assertEqual(0, metrics["failed"])
        self.assertEqual(1, metrics["by_name"]["SuccessCommand"]["executed"])
        self.assertEqual({}, metrics["by_sub_module"])

    def test_execute_failure_updates_metrics(self):
        """失敗実行時に失敗メトリクスと履歴が更新されることを確認する。"""
        ShareParameter.dry_run_mode = False
        command = FailureCommand(None)

        with self.assertRaises(RuntimeError):
            command.execute()

        metrics = ShareParameter.command_metrics
        self.assertEqual(1, metrics["total"])
        self.assertEqual(0, metrics["succeeded"])
        self.assertEqual(1, metrics["failed"])
        self.assertEqual(1, metrics["by_name"]["FailureCommand"]["executed"])
        self.assertEqual(1, metrics["by_name"]["FailureCommand"]["failed"])
        self.assertEqual("FailureCommand", metrics["failures"][0]["command_name"])
        self.assertIsNone(metrics["failures"][0]["sub_module_name"])
        self.assertEqual("RuntimeError", metrics["failures"][0]["error_type"])
        self.assertIn("failed_at", metrics["failures"][0])
        self.assertEqual(0, metrics["failures"][0]["tries_count"])

    def test_execute_updates_sub_module_metrics(self):
        """サブモジュール名がある場合に by_sub_module が更新されることを確認する。"""
        ShareParameter.dry_run_mode = False
        ShareParameter.current_sub_module_name = "SampleSubModule"
        command = SuccessCommand()

        command.execute()

        metrics = ShareParameter.command_metrics
        self.assertIn("SampleSubModule", metrics["by_sub_module"])
        sub_module_metrics = metrics["by_sub_module"]["SampleSubModule"]
        self.assertEqual(1, sub_module_metrics["total"])
        self.assertEqual(1, sub_module_metrics["succeeded"])
        self.assertEqual(0, sub_module_metrics["failed"])
        self.assertEqual(1, sub_module_metrics["by_name"]["SuccessCommand"]["executed"])
