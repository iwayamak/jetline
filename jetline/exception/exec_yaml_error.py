"""実行 YAML 構造エラー例外。."""


class ExecYamlError(Exception):
    """実行 YAML が不正な場合に送出する例外。."""

    def __init__(self, info):
        """例外情報を保持する。."""
        self._info = info

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
