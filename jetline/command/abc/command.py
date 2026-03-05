
"""コマンド実行の共通テンプレート。."""

import logging
import time
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ...container.component.abc.component import Component
from ...share_parameter.share_parameter import ShareParameter

logger = logging.getLogger('jetline')


@dataclass
class CommandExecutionState:
    """コマンド実行結果を保持する。."""

    succeeded: bool = False
    error: Exception | None = None


class Command(metaclass=ABCMeta):
    """set_up → body → run（または dry_run）→ tear_down の順序を提供する。."""

    def __init__(self, component: Component | None):
        """コマンドを初期化する。.

        Args:
            component: 利用するコンポーネント。不要なコマンドでは `None`。
        """
        self.component = component
        self._state = CommandExecutionState()

    @property
    def state(self) -> CommandExecutionState:
        """直近実行の状態を返す。."""
        return self._state

    @property
    def command_name(self) -> str:
        """コマンド名を返す。."""
        return self.__class__.__name__

    def set_up(self):
        """実行前処理を行う。."""
        logger.debug('%s set_up', self.command_name)

    def body(self):
        """実行本体の事前処理を行う。."""
        logger.debug('%s body', self.command_name)

    @abstractmethod
    def run(self):
        """通常実行時の処理を行う。."""
        raise NotImplementedError

    @abstractmethod
    def dry_run(self):
        """ドライラン実行時の処理を行う。."""
        raise NotImplementedError

    def tear_down(self):
        """実行後処理を行う。."""
        logger.debug('%s tear_down', self.command_name)

    def execute(self):
        """コマンド本体を実行する。"""
        logger.debug('%s execute start', self.command_name)
        self._state = CommandExecutionState()
        started_at = time.perf_counter()
        self._record_command_start()
        try:
            self.set_up()
            self.body()
            if ShareParameter.dry_run_mode:
                self.dry_run()
            else:
                self.run()
        except Exception as exc:
            self._state.error = exc
            self._record_command_failure(exc)
            logger.exception('%s execute failed', self.command_name)
            raise
        else:
            self._state.succeeded = True
            self._record_command_success()
        finally:
            self.tear_down()
            self._record_command_elapsed_seconds(time.perf_counter() - started_at)
            logger.debug('%s execute end (succeeded=%s)', self.command_name, self._state.succeeded)

    def _record_command_start(self) -> None:
        """コマンド実行開始をメトリクスへ記録する。"""
        metrics = self._ensure_command_metrics()
        metrics["total"] = int(metrics.get("total", 0)) + 1
        by_name = self._ensure_by_name(metrics)
        command_metric = by_name.setdefault(
            self.command_name,
            {"executed": 0, "succeeded": 0, "failed": 0, "elapsed_seconds_total": 0.0},
        )
        command_metric["executed"] = int(command_metric.get("executed", 0)) + 1
        self._record_sub_module_metric_start(metrics)

    def _record_command_success(self) -> None:
        """コマンド成功をメトリクスへ記録する。"""
        metrics = self._ensure_command_metrics()
        metrics["succeeded"] = int(metrics.get("succeeded", 0)) + 1
        command_metric = self._ensure_command_metric(metrics)
        command_metric["succeeded"] = int(command_metric.get("succeeded", 0)) + 1
        self._record_sub_module_metric_success(metrics)

    def _record_command_failure(self, error: Exception) -> None:
        """コマンド失敗をメトリクスへ記録する。

        Args:
            error: 発生した例外。
        """
        metrics = self._ensure_command_metrics()
        metrics["failed"] = int(metrics.get("failed", 0)) + 1
        command_metric = self._ensure_command_metric(metrics)
        command_metric["failed"] = int(command_metric.get("failed", 0)) + 1
        self._record_sub_module_metric_failure(metrics)
        failures = self._ensure_failures(metrics)
        sub_module_name = ShareParameter.current_sub_module_name
        failures.append(
            {
                "command_name": self.command_name,
                "sub_module_name": sub_module_name,
                "error_type": error.__class__.__name__,
                "error_message": str(error),
                "failed_at": datetime.now().isoformat(timespec="seconds"),
                "tries_count": ShareParameter.tries_count,
            }
        )

    def _record_command_elapsed_seconds(self, elapsed_seconds: float) -> None:
        """コマンド実行時間をメトリクスへ加算する。

        Args:
            elapsed_seconds: 実行時間（秒）。
        """
        metrics = self._ensure_command_metrics()
        command_metric = self._ensure_command_metric(metrics)
        command_metric["elapsed_seconds_total"] = float(
            command_metric.get("elapsed_seconds_total", 0.0)
        ) + elapsed_seconds
        self._record_sub_module_metric_elapsed(metrics, elapsed_seconds)

    @staticmethod
    def _ensure_command_metrics() -> dict[str, Any]:
        """共有領域にコマンドメトリクス辞書を初期化して返す。"""
        metrics = ShareParameter.command_metrics
        if not isinstance(metrics, dict):
            metrics = {}
            ShareParameter.command_metrics = metrics
        return metrics

    @staticmethod
    def _ensure_by_name(metrics: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """コマンド名別メトリクス辞書を返す。"""
        by_name = metrics.get("by_name")
        if not isinstance(by_name, dict):
            by_name = {}
            metrics["by_name"] = by_name
        return by_name

    @staticmethod
    def _ensure_by_sub_module(metrics: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """サブモジュール名別メトリクス辞書を返す。"""
        by_sub_module = metrics.get("by_sub_module")
        if not isinstance(by_sub_module, dict):
            by_sub_module = {}
            metrics["by_sub_module"] = by_sub_module
        return by_sub_module

    @staticmethod
    def _ensure_failures(metrics: dict[str, Any]) -> list[dict[str, Any]]:
        """失敗履歴リストを返す。"""
        failures = metrics.get("failures")
        if not isinstance(failures, list):
            failures = []
            metrics["failures"] = failures
        return failures

    def _ensure_command_metric(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """当該コマンドのメトリクス辞書を返す。"""
        by_name = self._ensure_by_name(metrics)
        return by_name.setdefault(
            self.command_name,
            {"executed": 0, "succeeded": 0, "failed": 0, "elapsed_seconds_total": 0.0},
        )

    def _record_sub_module_metric_start(self, metrics: dict[str, Any]) -> None:
        """サブモジュール単位の開始メトリクスを記録する。"""
        sub_module_metric = self._ensure_sub_module_metric(metrics)
        if sub_module_metric is None:
            return
        sub_module_metric["total"] = int(sub_module_metric.get("total", 0)) + 1
        by_name = sub_module_metric.setdefault("by_name", {})
        command_metric = by_name.setdefault(
            self.command_name,
            {"executed": 0, "succeeded": 0, "failed": 0, "elapsed_seconds_total": 0.0},
        )
        command_metric["executed"] = int(command_metric.get("executed", 0)) + 1

    def _record_sub_module_metric_success(self, metrics: dict[str, Any]) -> None:
        """サブモジュール単位の成功メトリクスを記録する。"""
        sub_module_metric = self._ensure_sub_module_metric(metrics)
        if sub_module_metric is None:
            return
        sub_module_metric["succeeded"] = int(sub_module_metric.get("succeeded", 0)) + 1
        command_metric = sub_module_metric["by_name"][self.command_name]
        command_metric["succeeded"] = int(command_metric.get("succeeded", 0)) + 1

    def _record_sub_module_metric_failure(self, metrics: dict[str, Any]) -> None:
        """サブモジュール単位の失敗メトリクスを記録する。"""
        sub_module_metric = self._ensure_sub_module_metric(metrics)
        if sub_module_metric is None:
            return
        sub_module_metric["failed"] = int(sub_module_metric.get("failed", 0)) + 1
        command_metric = sub_module_metric["by_name"][self.command_name]
        command_metric["failed"] = int(command_metric.get("failed", 0)) + 1

    def _record_sub_module_metric_elapsed(
        self,
        metrics: dict[str, Any],
        elapsed_seconds: float,
    ) -> None:
        """サブモジュール単位の実行時間を記録する。"""
        sub_module_metric = self._ensure_sub_module_metric(metrics)
        if sub_module_metric is None:
            return
        command_metric = sub_module_metric["by_name"][self.command_name]
        command_metric["elapsed_seconds_total"] = float(
            command_metric.get("elapsed_seconds_total", 0.0)
        ) + elapsed_seconds

    def _ensure_sub_module_metric(self, metrics: dict[str, Any]) -> dict[str, Any] | None:
        """現在のサブモジュールに対応するメトリクス辞書を返す。"""
        sub_module_name = ShareParameter.current_sub_module_name
        if not sub_module_name:
            return None
        by_sub_module = self._ensure_by_sub_module(metrics)
        return by_sub_module.setdefault(
            sub_module_name,
            {"total": 0, "succeeded": 0, "failed": 0, "by_name": {}},
        )
