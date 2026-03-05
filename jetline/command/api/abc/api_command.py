
"""API 呼び出しを行うコマンド基底。."""

import logging
from typing import Any, cast

import requests

from ....command.abc.command import Command
from ....container.component.abc.component import Component

logger = logging.getLogger('jetline')


class ApiCommand(Command):
    """HTTP API 呼び出し処理の共通機能を提供する。."""

    def __init__(self, component: Component, timeout: int = 1800):
        """API コマンドを初期化する。.

        Args:
            component: API 接続先コンポーネント。
            timeout: リクエストタイムアウト秒。
        """
        self._session = requests.Session()
        self._response = None
        self._timeout = timeout
        self._url = None
        super().__init__(component)

    @property
    def api_component(self) -> Component:
        """API コンポーネントを返す。"""
        return cast(Component, self.component)

    @staticmethod
    def _resolve_component_url(component: Component) -> str:
        """コンポーネントから URL を解決する。

        Args:
            component: URL を保持する API コンポーネント。

        Returns:
            str: 接続先 URL。

        Raises:
            AttributeError: `url` 属性が存在しない場合。
        """
        try:
            return cast(Any, component).url
        except AttributeError as exc:
            raise AttributeError("api component must have 'url' attribute") from exc

    def set_up(self):
        """接続先 URL を解決し、ログを出力する。."""
        logger.info(f'headers: {self._session.headers}')

        self._url = self._resolve_component_url(self.api_component)
        logger.info(f'url: {self._url}')

        super().set_up()

    def body(self):
        """API 実行前処理を行う。."""

    def run(self):
        """API コマンド本体はサブクラスで実装する。."""
        raise NotImplementedError

    def dry_run(self):
        """ドライラン時は URL のみ解決済み状態にする。."""

    def tear_down(self):
        """セッションとレスポンスをクローズする。."""
        if self._session is not None:
            self._session.close()
        if self._response is not None:
            self._response.close()
        super().tear_down()

    def _api_get(self, **kwargs):
        """GET リクエストを実行する。."""
        return self._session.get(
            self._url,
            **kwargs
        )

    def _api_post(self, **kwargs):
        """POST リクエストを実行する。."""
        return self._session.post(
            self._url,
            **kwargs
        )

    def _api_put(self, **kwargs):
        """PUT リクエストを実行する。."""
        return self._session.put(
            self._url,
            **kwargs
        )

    def _api_delete(self, **kwargs):
        """DELETE リクエストを実行する。."""
        return self._session.delete(
            self._url,
            **kwargs
        )
