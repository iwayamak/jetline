"""標準ライブラリ関数を呼び出すコマンド基底。."""

import importlib
import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any

from ...container.component.abc.component import Component
from ..abc.command import Command

logger = logging.getLogger('jetline')


class BuiltInCommand(Command, metaclass=ABCMeta):
    """標準ライブラリの関数呼び出しをラップする。."""

    def __init__(
        self,
        component: Component | None,
        instance_name: str,
        attr_name: str,
    ):
        """BuiltIn コマンドを初期化する。.

        Args:
            component: コンポーネント。標準処理では通常 `None`。
            instance_name: import するモジュール名。
            attr_name: 実行する属性（関数）名。
        """
        self._instance_name = instance_name
        self._attr_name = attr_name
        super().__init__(component)

    def set_up(self):
        """実行前処理を行う。."""
        pass

    def body(self):
        """実行本体の事前処理を行う。."""
        pass

    def run(self):
        """実処理を実行する。."""
        self._log_target()
        self._run_target_callable(self._resolve_target_callable())

    def dry_run(self):
        """ドライラン時に実行対象を出力する。."""
        self._log_target()

    def tear_down(self):
        """実行後処理を行う。."""
        pass

    def _log_target(self):
        """実行対象モジュールと属性をログ出力する。."""
        logger.info(
            'instance_name: %s  attr_name: %s',
            self._instance_name,
            self._attr_name,
        )

    def _resolve_target_callable(self) -> Callable[..., Any]:
        """実行対象の関数オブジェクトを返す。."""
        obj = importlib.import_module(self._instance_name)
        return getattr(obj, self._attr_name)

    @abstractmethod
    def _run_target_callable(self, target_callable: Callable[..., Any]) -> None:
        """関数呼び出し本体を実装する。."""
