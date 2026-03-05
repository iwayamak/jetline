"""FileSyncError のユニットテスト。."""

from jetline.exception.file_sync_error import FileSyncError
from test.abc.base_test_case import BaseTestCase


class TestFileSyncError(BaseTestCase):
    """FileSyncError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """FileSyncError が送出できることを確認する。."""
        with self.assertRaises(FileSyncError):
            raise FileSyncError("file sync error")
