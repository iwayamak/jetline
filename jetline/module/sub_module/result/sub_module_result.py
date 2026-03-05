"""サブモジュール実行結果の集約モデル。."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ....share_parameter.share_parameter import ShareParameter

TimestampLike = datetime | str


@dataclass
class SubModuleLogDataFile:
    """1実行分のファイル結果を保持する。."""

    local: list[str]
    s3: list[str]


@dataclass
class SubModuleLogRecord:
    """1実行分のサブモジュール実行ログを保持する。."""

    sub_module_name: str
    data_file: SubModuleLogDataFile
    status: str
    start_time: TimestampLike
    end_time: TimestampLike
    processing_time: float


class SubModuleResult:
    """サブモジュール実行結果を時系列で保持する。."""

    FILE_NAME_SUFFIX = "_result.yaml"
    KEY_SETTINGS_YAML_RESULT_DIR = "result_dir"
    KEY_BATCH_NAME = "batch_name"
    KEY_LOG = "log"
    KEY_SUB_MODULE_NAME = "sub_module_name"
    KEY_DATA_FILE = "data_file"
    KEY_DATA_FILE_S3 = "s3"
    KEY_DATA_FILE_LOCAL = "local"
    KEY_STATUS = "status"
    KEY_UPDATE_TS = "update_ts"
    KEY_START_TIME = "start_time"
    KEY_END_TIME = "end_time"
    KEY_PROCESSING_TIME = "processing_time"
    KEY_METADATA = "metadata"
    KEY_CREATOR_METRICS = "sub_module_creator_metrics"
    KEY_COMMAND_METRICS = "command_metrics"
    KEY_SUB_MODULE_SUMMARY = "sub_module_summary"
    KEY_EXECUTION_CONTEXT = "execution_context"
    C_COMPONENT = "c_component"
    C_TABLE_NAME = "c_table_name"
    C_COLUMNS = "c_columns"
    STATUS_SUCCESS = "success"
    STATUS_ERROR = "error"

    def __init__(self):
        """実行結果コンテナを初期化する。."""
        self._batch_name = ShareParameter.batch_name
        self._log_records: list[SubModuleLogRecord] = []
        self._metadata: dict[str, Any] = {}

    def append_result(
        self,
        sub_module_name: str,
        start_time: TimestampLike,
        end_time: TimestampLike,
        processing_time: float,
        local_data_file_list: list[str] | None = None,
        s3_data_file_list: list[str] | None = None,
        status: str = STATUS_SUCCESS,
    ) -> None:
        """サブモジュール実行結果を末尾に追加する。.

        Args:
            sub_module_name: サブモジュール名。
            start_time: 開始時刻。
            end_time: 終了時刻。
            processing_time: 処理時間（秒）。
            local_data_file_list: ローカルファイル一覧。
            s3_data_file_list: S3 ファイル一覧。
            status: 実行ステータス。
        """
        local_data_files = [] if local_data_file_list is None else list(local_data_file_list)
        s3_data_files = [] if s3_data_file_list is None else list(s3_data_file_list)
        record = SubModuleLogRecord(
            sub_module_name=sub_module_name,
            data_file=SubModuleLogDataFile(local=local_data_files, s3=s3_data_files),
            status=status,
            start_time=start_time,
            end_time=end_time,
            processing_time=processing_time,
        )
        self._log_records.append(record)

    def as_dict(self) -> dict[str, Any]:
        """YAML 出力互換の辞書形式へ変換する。."""
        result = {
            self.KEY_BATCH_NAME: self._batch_name,
            self.KEY_LOG: [self._record_to_dict(record) for record in self._log_records],
        }
        if self._metadata:
            result[self.KEY_METADATA] = dict(self._metadata)
        return result

    def set_creator_metrics(self, metrics: dict[str, int]) -> None:
        """SubModuleCreator の統計情報を記録する。

        Args:
            metrics: ロード統計辞書。
        """
        self._metadata[self.KEY_CREATOR_METRICS] = dict(metrics)

    def set_command_metrics(self, metrics: dict[str, Any]) -> None:
        """Command 実行統計を記録する。

        Args:
            metrics: コマンド実行統計辞書。
        """
        self._metadata[self.KEY_COMMAND_METRICS] = dict(metrics)

    def set_sub_module_summary(self, summary: dict[str, Any]) -> None:
        """SubModule 単位の要約情報を記録する。

        Args:
            summary: サブモジュール単位の要約辞書。
        """
        self._metadata[self.KEY_SUB_MODULE_SUMMARY] = dict(summary)

    def set_execution_context(self, execution_context: dict[str, Any]) -> None:
        """実行コンテキスト情報を記録する。

        Args:
            execution_context: 実行再現に必要なメタ情報。
        """
        self._metadata[self.KEY_EXECUTION_CONTEXT] = dict(execution_context)

    @staticmethod
    def build_sub_module_summary(command_metrics: dict[str, Any]) -> dict[str, Any]:
        """コマンド実行統計から SubModule 単位の要約を構築する。

        Args:
            command_metrics: `command_metrics` 辞書。

        Returns:
            dict[str, Any]: サブモジュールごとの要約辞書。
        """
        by_sub_module = command_metrics.get("by_sub_module")
        if not isinstance(by_sub_module, dict):
            return {}

        summary: dict[str, Any] = {}
        for sub_module_name, sub_module_metrics in by_sub_module.items():
            if not isinstance(sub_module_metrics, dict):
                continue
            by_name = sub_module_metrics.get("by_name")
            if not isinstance(by_name, dict):
                by_name = {}
            elapsed_seconds_total = 0.0
            failed_commands: list[str] = []
            for command_name, command_metrics_per_name in by_name.items():
                if not isinstance(command_metrics_per_name, dict):
                    continue
                elapsed_seconds_total += float(
                    command_metrics_per_name.get("elapsed_seconds_total", 0.0)
                )
                if int(command_metrics_per_name.get("failed", 0)) > 0:
                    failed_commands.append(command_name)

            total = int(sub_module_metrics.get("total", 0))
            succeeded = int(sub_module_metrics.get("succeeded", 0))
            failed = int(sub_module_metrics.get("failed", 0))
            success_rate = 0.0 if total == 0 else round((succeeded / total) * 100, 2)
            summary[sub_module_name] = {
                "total": total,
                "succeeded": succeeded,
                "failed": failed,
                "success_rate": success_rate,
                "elapsed_seconds_total": round(elapsed_seconds_total, 6),
                "failed_commands": sorted(failed_commands),
            }
        return summary

    def get_metadata(self) -> dict[str, Any]:
        """記録済みメタデータを返す。"""
        return dict(self._metadata)

    def get_last_log(self) -> dict[str, Any] | None:
        """最後に追加されたログを辞書形式で返す。."""
        record = self._get_last_record()
        if record is None:
            return None
        return self._record_to_dict(record)

    def get_last_value(self, key: str) -> Any:
        """最後に追加されたログの指定キーを返す。."""
        last_log = self.get_last_log()
        if last_log is None:
            return None
        return last_log.get(key)

    def get_last_log_sub_module_name(self) -> str | None:
        """最後のサブモジュール名を返す。."""
        return self.get_last_value(self.KEY_SUB_MODULE_NAME)

    def get_last_log_processing_time(self) -> float | None:
        """最後の処理時間を返す。."""
        return self.get_last_value(self.KEY_PROCESSING_TIME)

    def get_last_log_status(self) -> str | None:
        """最後のステータスを返す。."""
        return self.get_last_value(self.KEY_STATUS)

    def get_last_log_start_time(self) -> TimestampLike | None:
        """最後の開始時刻を返す。."""
        return self.get_last_value(self.KEY_START_TIME)

    def get_last_log_end_time(self) -> TimestampLike | None:
        """最後の終了時刻を返す。."""
        return self.get_last_value(self.KEY_END_TIME)

    def get_last_log_data_file(self) -> dict[str, list[str]] | None:
        """最後のファイル情報辞書を返す。."""
        return self.get_last_value(self.KEY_DATA_FILE)

    def get_last_log_local_data_file_list(self) -> list[str] | None:
        """最後のローカルファイル一覧を返す。."""
        data_file = self.get_last_log_data_file()
        if data_file is None:
            return None
        return data_file[self.KEY_DATA_FILE_LOCAL]

    def get_last_log_s3_data_file_list(self) -> list[str] | None:
        """最後の S3 ファイル一覧を返す。."""
        data_file = self.get_last_log_data_file()
        if data_file is None:
            return None
        return data_file[self.KEY_DATA_FILE_S3]

    def _get_last_record(self) -> SubModuleLogRecord | None:
        """最後に追加されたログレコードを返す。."""
        if len(self._log_records) < 1:
            return None
        return self._log_records[-1]

    def _record_to_dict(self, record: SubModuleLogRecord) -> dict[str, Any]:
        """ログレコードを辞書形式へ変換する。."""
        return {
            self.KEY_SUB_MODULE_NAME: record.sub_module_name,
            self.KEY_DATA_FILE: {
                self.KEY_DATA_FILE_LOCAL: record.data_file.local,
                self.KEY_DATA_FILE_S3: record.data_file.s3,
            },
            self.KEY_STATUS: record.status,
            self.KEY_START_TIME: record.start_time,
            self.KEY_END_TIME: record.end_time,
            self.KEY_PROCESSING_TIME: record.processing_time,
        }
