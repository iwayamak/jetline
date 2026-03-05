"""未定義テンプレート本文エラー例外。."""


class UndefinedBodyStringError(Exception):
    """未定義の本文文字列が参照された場合に送出する例外。."""

    def __init__(self, body_str):
        """未定義本文文字列を保持する。."""
        self._info = f"undefined body string: {body_str} see Template.SUB_STR!!"

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
