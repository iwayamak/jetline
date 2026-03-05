"""コマンド実行失敗例外。."""


class CommandError(Exception):
    """コマンド実行が失敗した場合に送出する例外。."""

    def __init__(self, return_code=None, cmd=None):
        """終了コードとコマンド文字列から例外情報を生成する。."""
        info = "Command '{cmd}' returned non-zero exit status {return_code}"
        self._info = info.format(cmd=cmd, return_code=return_code)

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
