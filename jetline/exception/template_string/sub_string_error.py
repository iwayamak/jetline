"""テンプレート文字列エラー例外。."""


class TemplateStringError(Exception):
    """テンプレート全体が不正な場合に送出する例外。."""

    def __init__(self, info):
        """例外情報を保持する。."""
        self._info = info

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
