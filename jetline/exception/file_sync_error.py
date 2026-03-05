"""ファイル同期処理エラー例外。."""


class FileSyncError(Exception):
    """ファイル同期処理失敗時に送出する例外。."""

    def __init__(self, info):
        """例外情報を保持する。."""
        self._info = info

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
