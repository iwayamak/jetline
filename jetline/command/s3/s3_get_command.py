"""S3 オブジェクト取得コマンド。."""

from ...container.component.s3_component import S3Component
from .abc.s3_command import S3Command


class S3GetCommand(S3Command):
    """S3 オブジェクトをローカルファイルへ取得する。."""

    def __init__(self, component: S3Component, key: str, file_path: str):
        """S3 取得コマンドを初期化する。.

        Args:
            component: S3 コンポーネント。
            key: S3 オブジェクトキー。
            file_path: 保存先ローカルパス。
        """
        self._key = key
        self._file_path = file_path
        super().__init__(component)

    def run(self):
        """S3 オブジェクトをダウンロードする。."""
        super().run()
        self._bucket.download_file(self._key, self._file_path)
