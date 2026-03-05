"""テンプレート本文文字列エラー例外。."""


class BodyStringError(Exception):
    """テンプレート本文が不正な場合に送出する例外。."""

    def __init__(self, body_str):
        """不正な本文文字列を保持する。."""
        self._info = (
            f"invalid body str: {body_str} "
            "body str is inner string of template string. like this ${<body string>}."
        )

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
