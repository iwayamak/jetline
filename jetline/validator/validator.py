"""sub_module_parameter の値検証デコレータ群。."""

import os.path
import re
from functools import wraps
from typing import Any

from ..container.container import Container
from ..exception.sub_module_parameter_error import SubModuleParameterError


class Validator:
    """各種値検証デコレータを提供する。."""

    @staticmethod
    def _extract_target(args: tuple[Any, ...]) -> Any:
        """デコレータ対象値を抽出する。.

        Args:
            args: デコレータへ渡された位置引数。

        Returns:
            Any: 検証対象値。
        """
        if len(args) > 1:
            return args[1]
        return args[0]

    @staticmethod
    def _strtobool(value: Any) -> bool:
        """`distutils.util.strtobool` 相当の真偽値変換を行う。.

        Args:
            value: 判定対象値。

        Returns:
            bool: 変換結果。

        Raises:
            ValueError: 真偽値として解釈できない場合。
        """
        if not isinstance(value, str):
            raise ValueError(f"invalid truth value type: {type(value)}")

        lowered = value.strip().lower()
        if lowered in {"y", "yes", "t", "true", "on", "1"}:
            return True
        if lowered in {"n", "no", "f", "false", "off", "0"}:
            return False
        raise ValueError(f"invalid truth value: {value}")

    @staticmethod
    def component_key(func):
        """コンポーネントキー形式を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = Validator._extract_target(args)
            if key is None:
                return func(*args, **kwargs)
            try:
                Container.component(key)
            except Exception as exc:
                raise SubModuleParameterError("component_key", key) from exc
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def path(func):
        """パス存在を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            path_str = Validator._extract_target(args)
            if path_str is None:
                return func(*args, **kwargs)
            if not os.path.exists(path_str):
                raise SubModuleParameterError("file_path", path_str)
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def digit(func):
        """整数値を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            value = Validator._extract_target(args)
            if value is None:
                return func(*args, **kwargs)
            if not isinstance(value, int) and not str(value).isdigit():
                raise SubModuleParameterError("digit", value)
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def boolean(func):
        """真偽値を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            value = Validator._extract_target(args)
            if value is None:
                return func(*args, **kwargs)
            if not isinstance(value, bool):
                try:
                    Validator._strtobool(value)
                except ValueError as exc:
                    raise SubModuleParameterError("boolean", value) from exc
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def regexp(pattern):
        """正規表現一致を検証するデコレータを生成する。."""

        def _regexp(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                value = Validator._extract_target(args)
                if value is None:
                    return func(*args, **kwargs)
                matched = re.search(pattern, str(value), re.MULTILINE)
                if matched is None:
                    raise SubModuleParameterError(f"regexp:{pattern}", value)
                return func(*args, **kwargs)

            return wrapper

        return _regexp

    @staticmethod
    def range(lower, upper):
        """数値範囲を検証するデコレータを生成する。."""

        def _range(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                value = Validator._extract_target(args)
                if value is None:
                    return func(*args, **kwargs)
                try:
                    if value < lower or value > upper:
                        raise SubModuleParameterError(f"range [{lower}] to [{upper}]", value)
                except TypeError as exc:
                    raise SubModuleParameterError(f"range [{lower}] to [{upper}]", value) from exc
                return func(*args, **kwargs)

            return wrapper

        return _range

    @staticmethod
    def list(func):
        """リスト型を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            value = Validator._extract_target(args)
            if value is None:
                return func(*args, **kwargs)
            if not isinstance(value, list):
                raise SubModuleParameterError("list", value)
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def dict(func):
        """辞書型を検証する。."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            value = Validator._extract_target(args)
            if value is None:
                return func(*args, **kwargs)
            if not isinstance(value, dict):
                raise SubModuleParameterError("dict", value)
            return func(*args, **kwargs)

        return wrapper
