"""PostgreSQL コンポーネント実装。."""

import copy
import logging

from .abc.component import Component

logger = logging.getLogger("jetline")


class PostgreSQLComponent(Component):
    """PostgreSQL 接続設定を保持するコンポーネント。."""

    def __init__(self, param: dict):
        """接続設定を初期化する。."""
        self._user = param.get("user")
        self._password = param.get("password")
        self._host = param.get("host")
        self._port = param.get("port")
        self._database = param.get("database")
        self._schema = param.get("schema")
        super().__init__()

    def _validation(self):
        """必須設定の欠損を検証する。."""
        if (
            self._user is None
            or self._password is None
            or self._host is None
            or self._port is None
            or self._database is None
            or self._schema is None
        ):
            raise Exception("user / password / host / port / database / schema is None!")

    @property
    def user(self):
        """接続ユーザーを返す。."""
        return self._user

    @property
    def password(self):
        """接続パスワードを返す。."""
        return self._password

    @property
    def host(self):
        """接続先ホストを返す。."""
        return self._host

    @property
    def port(self):
        """接続先ポートを返す。."""
        return self._port

    @property
    def database(self):
        """接続先データベース名を返す。."""
        return self._database

    @property
    def schema(self):
        """デフォルトスキーマ名を返す。."""
        return self._schema

    @classmethod
    def create_component(cls, param: dict) -> "PostgreSQLComponent":
        """設定辞書からコンポーネントを生成する。."""
        instance = cls(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        """マスク済み情報をログ出力する。."""
        log_dict = copy.deepcopy(instance_dict)
        log_dict["_password"] = "****"
        logger.info("created %s", cls.__name__)
        logger.info(log_dict)
