"""S3 オブジェクト送信コマンド。."""

from ...container.component.s3_component import S3Component
from .abc.s3_command import S3Command


class S3PutCommand(S3Command):
    """ローカルファイルを S3 へアップロードする。."""

    def __init__(self, component: S3Component, file_path: str, key: str):
        """S3 送信コマンドを初期化する。.

        Args:
            component: S3 コンポーネント。
            file_path: 送信元ローカルファイル。
            key: 送信先 S3 オブジェクトキー。
        """
        self._file_path = file_path
        self._key = key
        super().__init__(component)

    def run(self):
        """ローカルファイルを S3 へ送信する。."""
        super().run()
        self._bucket.upload_file(self._file_path, self._key)
