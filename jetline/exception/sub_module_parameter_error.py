"""サブモジュールパラメータ検証エラー例外。."""


class SubModuleParameterError(Exception):
    """パラメータ検証失敗時に送出する例外。."""

    def __init__(self, validator_name, target):
        """検証種別と対象値から例外情報を生成する。."""
        self._info = (
            "sub_module_parameter is invalid. "
            f"validator: {validator_name} target: {target}"
        )

    def __str__(self):
        """例外メッセージ文字列を返す。."""
        return repr(self._info)
