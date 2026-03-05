
"""任意 Python ロジックを実行するカスタムコマンド基底。."""

from abc import ABCMeta, abstractmethod

from ..abc.command import Command


class CustomCommand(Command, metaclass=ABCMeta):
    """プラグイン実装向けの共通コマンド基底。."""

    def __init__(self, kwargs: dict):
        """カスタムコマンドを初期化する。.

        Args:
            kwargs: プラグインへ渡す引数辞書。
        """
        self._kwargs = kwargs
        super().__init__(None)

    @abstractmethod
    def set_up(self):
        """実行前処理を行う。."""

    @abstractmethod
    def body(self):
        """実行本体前処理を行う。."""

    @abstractmethod
    def run(self):
        """通常実行処理を行う。."""

    @abstractmethod
    def dry_run(self):
        """ドライラン実行処理を行う。."""

    @abstractmethod
    def tear_down(self):
        """実行後処理を行う。."""
