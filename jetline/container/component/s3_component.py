"""S3 コンポーネント実装。."""

import copy
import logging

from .abc.component import Component

logger = logging.getLogger("jetline")


class S3Component(Component):
    """S3 接続設定を保持するコンポーネント。."""

    def __init__(self, param: dict):
        """S3 接続設定を初期化する。."""
        self._bucket = param.get("bucket")
        self._aws_access_key = param.get("aws_access_key")
        self._aws_secret_access_key = param.get("aws_secret_access_key")
        self._region_name = param.get("region_name")
        super().__init__()

    def _validation(self):
        """必須設定の欠損を検証する。."""
        if (
            self._bucket is None
            or self._aws_access_key is None
            or self._aws_secret_access_key is None
            or self._region_name is None
        ):
            raise Exception(
                "bucket / aws_access_key / aws_secret_access_key / region_name is None!"
            )

    @property
    def bucket(self):
        """バケット名を返す。."""
        return self._bucket

    @property
    def aws_access_key(self):
        """アクセスキーを返す。."""
        return self._aws_access_key

    @property
    def aws_secret_access_key(self):
        """シークレットアクセスキーを返す。."""
        return self._aws_secret_access_key

    @property
    def region_name(self):
        """リージョン名を返す。."""
        return self._region_name

    @classmethod
    def create_component(cls, param: dict) -> "S3Component":
        """設定辞書からコンポーネントを生成する。."""
        instance = cls(param)
        cls._output_log(instance.__dict__)
        return instance

    @classmethod
    def _output_log(cls, instance_dict: dict):
        """マスク済み情報をログ出力する。."""
        log_dict = copy.deepcopy(instance_dict)
        log_dict["_aws_secret_access_key"] = "****"
        logger.info("created %s", cls.__name__)
        logger.info(log_dict)
