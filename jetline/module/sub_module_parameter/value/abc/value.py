"""パラメータ値ラッパーの基底クラス。."""


class Value:
    """サブモジュールパラメータ値を保持する。."""

    def __init__(self, value, display):
        """値ラッパーを初期化する。."""
        self._value = value
        self._display = display

    def get(self):
        """保持している値を返す。."""
        return self._value

    @property
    def display(self):
        """表示名を返す。未設定時は空文字を返す。."""
        return "" if self._display is None else self._display
