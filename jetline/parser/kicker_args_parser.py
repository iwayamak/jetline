
"""CLI 引数を解釈し、実行設定へ変換する。."""

import argparse
import ast
import datetime
from dataclasses import dataclass

JitterType = int | float | tuple[int | float, int | float]


@dataclass(frozen=True)
class RetryOptions:
    """リトライ設定。."""

    tries: int
    delay: int
    backoff: int
    jitter: JitterType
    max_delay: int | None


@dataclass(frozen=True)
class RunOptions:
    """ジョブ実行設定。."""

    yaml_file: str
    exec_date: str
    dry_run: bool
    working_dir: str | None
    retry: RetryOptions


class KickerArgsParser:
    """CLI 引数を実行設定へ変換するパーサ。."""

    def __init__(self, args):
        """引数を解析し、実行設定を構築する。.

        Args:
            args: CLI引数配列。
        """
        parser = argparse.ArgumentParser(
            prog='jetline',
            description='Jetline ETL runner',
        )
        parser.add_argument(
            '-y', '--yaml', dest='yaml_file', required=True,
            help='yaml ファイルパス。'
        )
        parser.add_argument(
            '-d', '--exec-date', dest='exec_date', type=KickerArgsParser._parse_exec_date,
            default=datetime.datetime.now().strftime('%Y%m%d'),
            help='実行日。形式は yyyymmdd（例: 20260401）'
        )
        parser.add_argument(
            '-D', '--dry-run', action='store_true', default=False,
            help='dry-run で実行する'
        )
        parser.add_argument(
            '-w', '--working-dir', dest='working_dir', default=None,
            help='実行時の作業ディレクトリ'
        )
        parser.add_argument(
            '-t', '--tries', dest='tries', type=KickerArgsParser._positive_int, default=1,
            help='最大試行回数（1以上）'
        )
        parser.add_argument(
            '-l', '--delay', dest='delay', type=KickerArgsParser._non_negative_int, default=1,
            help='初回待機秒（0以上）'
        )
        parser.add_argument(
            '-b', '--backoff', dest='backoff', type=KickerArgsParser._positive_int, default=1,
            help='待機秒の倍率（1以上）'
        )
        parser.add_argument(
            '-j', '--jitter', dest='jitter', type=KickerArgsParser._parse_jitter, default=0,
            help='待機秒の揺らぎ。数値または範囲（例: "(1, 3)"）'
        )
        parser.add_argument(
            '-m', '--max-delay',
            dest='max_delay',
            type=KickerArgsParser._non_negative_int,
            default=None,
            help='最大待機秒（0以上）'
        )

        parsed_args = parser.parse_args(args)
        self._options = RunOptions(
            yaml_file=parsed_args.yaml_file,
            exec_date=parsed_args.exec_date,
            dry_run=parsed_args.dry_run,
            working_dir=parsed_args.working_dir,
            retry=RetryOptions(
                tries=parsed_args.tries,
                delay=parsed_args.delay,
                backoff=parsed_args.backoff,
                jitter=parsed_args.jitter,
                max_delay=parsed_args.max_delay,
            ),
        )

    def options(self):
        """実行設定を返す。.

        Returns:
            RunOptions: 解析済み設定。
        """
        return self._options

    # 後方互換のため、従来アクセサを残す。
    def exec_yaml_path(self):
        """実行YAMLファイルパスを返す。."""
        return self._options.yaml_file

    def exec_date(self):
        """実行日を返す。."""
        return self._options.exec_date

    def working_dir(self):
        """作業ディレクトリを返す。."""
        return self._options.working_dir

    def dry_run(self):
        """ドライラン有効フラグを返す。."""
        return self._options.dry_run

    def tries(self):
        """最大試行回数を返す。."""
        return self._options.retry.tries

    def delay(self):
        """初回待機秒を返す。."""
        return self._options.retry.delay

    def backoff(self):
        """待機秒の倍率を返す。."""
        return self._options.retry.backoff

    def jitter(self):
        """待機秒の揺らぎ設定を返す。."""
        return self._options.retry.jitter

    def max_delay(self):
        """最大待機秒を返す。."""
        return self._options.retry.max_delay

    @staticmethod
    def _parse_exec_date(value):
        """実行日文字列を検証する。.

        Args:
            value: 検証対象の実行日。

        Returns:
            str: 検証済み実行日。
        """
        try:
            datetime.datetime.strptime(value, '%Y%m%d')
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                'exec-date は YYYYMMDD 形式で指定してください'
            ) from exc
        return value

    @staticmethod
    def _parse_jitter(raw_value):
        """Jitter 値を数値または範囲へ変換する。.

        Args:
            raw_value: CLI から受け取った文字列。

        Returns:
            JitterType: 数値または長さ2のタプル。
        """
        try:
            parsed = ast.literal_eval(raw_value)
        except (SyntaxError, ValueError):
            try:
                parsed = int(raw_value)
            except ValueError as exc:
                raise argparse.ArgumentTypeError(
                    'jitter は数値または (1, 3) のようなタプル/リストで指定してください'
                ) from exc

        if isinstance(parsed, (int, float)):
            return parsed
        if isinstance(parsed, (list, tuple)) and len(parsed) == 2 and all(
            isinstance(value, (int, float)) for value in parsed
        ):
            return tuple(parsed)
        raise argparse.ArgumentTypeError(
            'jitter は数値または (1, 3) のようなタプル/リストで指定してください'
        )

    @staticmethod
    def _positive_int(value):
        """1以上の整数であることを検証する。."""
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError('1以上の値を指定してください')
        return int_value

    @staticmethod
    def _non_negative_int(value):
        """0以上の整数であることを検証する。."""
        int_value = int(value)
        if int_value < 0:
            raise argparse.ArgumentTypeError('0以上の値を指定してください')
        return int_value
