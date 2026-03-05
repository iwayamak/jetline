"""サブモジュール読込失敗例外。."""


class SubModuleLoadError(Exception):
    """サブモジュール生成に失敗した場合に送出する例外。."""

    def __init__(self, sub_module_name):
        """失敗したサブモジュール名を保持する。."""
        self._info = f"Fail sub module load: {sub_module_name}"

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
