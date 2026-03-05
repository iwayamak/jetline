"""引数エラー例外。."""


class ArgumentError(Exception):
    """引数不正時に送出する例外。."""

    def __init__(self, info: str):
        """例外情報を初期化する。."""
        self._info = info

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
