"""コンポーネント読込失敗例外。."""


class ComponentLoadError(Exception):
    """コンポーネント生成に失敗した場合に送出する例外。."""

    def __init__(self, component_name):
        """失敗したコンポーネント名を保持する。."""
        self._info = f"Fail component load: {component_name}"

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
