"""S3 コマンドの共通基底。."""

import logging
from typing import cast

from boto3.session import Session

from ....command.abc.command import Command
from ....container.component.s3_component import S3Component

logger = logging.getLogger('jetline')


class S3Command(Command):
    """S3 バケット操作を行うコマンド基底クラス。."""

    def __init__(self, component: S3Component):
        """S3 コマンドを初期化する。.

        Args:
            component: S3 接続情報を持つコンポーネント。
        """
        self._bucket = None
        super().__init__(component)

    @property
    def s3_component(self) -> S3Component:
        """S3 コンポーネントを型付きで返す。"""
        return cast(S3Component, self.component)

    def set_up(self):
        """実行前処理を行う。."""
        super().set_up()

    def body(self):
        """実行本体の事前処理を行う。."""
        super().body()

    def run(self):
        """S3 バケットへ接続する。."""
        session = Session(
            aws_access_key_id=self.s3_component.aws_access_key,
            aws_secret_access_key=self.s3_component.aws_secret_access_key,
            region_name=self.s3_component.region_name,
        )
        s3 = session.resource('s3')
        self._bucket = s3.Bucket(self.s3_component.bucket)

    def dry_run(self):
        """ドライラン時の処理を行う。."""
        return None

    def tear_down(self):
        """実行後処理を行う。."""
        super().tear_down()
