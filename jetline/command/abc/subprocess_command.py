
"""サブプロセス実行コマンドの共通実装。."""

import logging
import subprocess
from abc import ABCMeta
from collections.abc import Sequence

from ...container.component.abc.component import Component
from ...exception.command_error import CommandError
from ..abc.command import Command

logger = logging.getLogger('jetline')


class SubprocessCommand(Command, metaclass=ABCMeta):
    """外部コマンドを実行し、戻り値や標準出力を保持する。."""

    def __init__(
        self,
        component: Component | None,
        cmd: Sequence[str],
        check: bool = True,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout: int = 43200,
    ):
        """サブプロセス実行コマンドを初期化する。.

        Args:
            component: 関連コンポーネント。
            cmd: 実行コマンド配列。
            check: True の場合は非0終了で例外化する。
            cwd: 実行ディレクトリ。
            env: 環境変数。
            timeout: タイムアウト秒。
        """
        self._cmd = [str(value) for value in cmd]
        self._check = check
        self._timeout = timeout
        self._return_code: int | None = None
        self._stdout: bytes | None = None
        self._cwd = cwd
        self._env = env
        super().__init__(component)

    @property
    def return_code(self) -> int | None:
        """直近実行時の終了コードを返す。."""
        return self._return_code

    @property
    def stdout(self) -> bytes | None:
        """直近実行時の標準出力を返す。."""
        return self._stdout

    def run(self):
        """サブプロセスを実行する。."""
        logger.info(f'command: {" ".join(self._cmd)}')
        if self._check:
            try:
                process = subprocess.run(
                    self._cmd,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=self._cwd,
                    env=self._env,
                    timeout=self._timeout,
                )
                self._stdout = process.stdout
                self._return_code = process.returncode
            except subprocess.CalledProcessError as exc:
                output = exc.output.decode('utf-8', errors='replace') if exc.output else ''
                logger.error(
                    f'subprocess error. return code:{exc.returncode}, output:{output}'
                )
                raise CommandError(
                    return_code=exc.returncode,
                    cmd=' '.join(self._cmd),
                ) from exc
        else:
            process = subprocess.run(
                self._cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self._cwd,
                env=self._env,
                timeout=self._timeout,
            )
            self._stdout = process.stdout
            self._return_code = process.returncode
        logger.info(f'subprocess return code: {self._return_code}')

    def dry_run(self):
        """ドライラン時に実行コマンドのみ出力する。."""
        logger.info(f'command: {" ".join(self._cmd)}')
