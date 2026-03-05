
"""コンポーネント基底クラス。."""

from abc import ABCMeta, abstractmethod


class Component(metaclass=ABCMeta):
    """各接続先コンポーネントの共通インターフェース。."""

    def __init__(self):
        """コンポーネントを初期化し、設定妥当性を検証する。."""
        self._validation()

    @abstractmethod
    def _validation(self):
        """コンポーネント設定の妥当性を検証する。."""

    @classmethod
    @abstractmethod
    def create_component(cls, param):
        """設定辞書からコンポーネントを生成する。."""

    @classmethod
    @abstractmethod
    def _output_log(cls, instance):
        """初期化済みコンポーネント情報をログへ出力する。."""
