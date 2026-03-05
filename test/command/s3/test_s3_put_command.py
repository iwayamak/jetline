"""S3PutCommand のユニットテスト."""

import os

from jetline.command.s3.s3_put_command import S3PutCommand
from jetline.container.container import Container

from ...abc.base_test_case import BaseTestCase


class TestS3PutCommand(BaseTestCase):
    """S3 へのアップロード処理を検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._component = Container().component("S3_COMPONENT.ID=UT")
        self._test_data_path = os.path.join(os.path.dirname(__file__), "test_data")
        super().__init__(*args, **kwargs)

    def test_s3_put(self) -> None:
        """ローカルファイルを S3 にアップロードできることを確認する."""
        file_path = os.path.join(self._test_data_path, "test_s3_put_command.tsv")
        command = S3PutCommand(self._component, file_path, os.path.basename(file_path))
        command.execute()
