"""SubModule パラメータ共通基底。."""


class SubModuleParameter:
    """プロパティ定義に基づいてパラメータを自動注入する基底クラス。."""

    def __init__(self, params: dict | None = None):
        """パラメータを初期化する。.

        Args:
            params: パラメータ辞書。未指定時は各プロパティに `None` を設定する。

        Raises:
            TypeError: `params` が辞書以外の場合。
        """
        if params is None:
            params = {}
        elif not isinstance(params, dict):
            raise TypeError('params must be a dict or None')

        for field_name in self._parameter_field_names():
            setattr(self, field_name, params.get(field_name))

    @classmethod
    def _parameter_field_names(cls) -> list[str]:
        """パラメータとして扱うプロパティ名一覧を返す。.

        継承階層を辿り、setter を持つ public property のみを対象とする。
        """
        field_names: list[str] = []
        for klass in reversed(cls.__mro__):
            for name, value in klass.__dict__.items():
                if name.startswith('_'):
                    continue
                if (
                    isinstance(value, property)
                    and value.fset is not None
                    and name not in field_names
                ):
                    field_names.append(name)
        return field_names
