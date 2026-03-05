"""SubModule と Parameter の生成を担うファクトリ."""

import importlib
import inspect
import re
import threading
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ...exception.sub_module_load_error import SubModuleLoadError
from ..sub_module.abc.sub_module import SubModule
from ..sub_module_parameter.abc.sub_module_parameter import SubModuleParameter


class SubModuleCreator:
    """クラス探索結果をキャッシュし、SubModule を高速に生成する."""

    _parameter_class_registry: dict[str, type[SubModuleParameter]] = {}
    _sub_module_class_registry: dict[str, type[SubModule]] = {}

    _parameter_module_index: dict[str, list[str]] | None = None
    _sub_module_module_index: dict[str, list[str]] | None = None

    _parameter_full_scan_done = False
    _sub_module_full_scan_done = False

    _metrics: dict[str, int] = {
        "lazy_hit": 0,
        "lazy_miss": 0,
        "full_scan_parameter": 0,
        "full_scan_sub_module": 0,
    }

    _registry_lock = threading.Lock()

    @classmethod
    def _ensure_indexes(cls) -> None:
        """モジュールインデックスを初期化する."""
        if cls._parameter_module_index is not None and cls._sub_module_module_index is not None:
            return

        with cls._registry_lock:
            if cls._parameter_module_index is None:
                package_root = Path(__file__).resolve().parents[1] / "sub_module_parameter"
                cls._parameter_module_index = cls._build_module_index(package_root)
            if cls._sub_module_module_index is None:
                package_root = Path(__file__).resolve().parent
                cls._sub_module_module_index = cls._build_module_index(package_root)

    @classmethod
    def _build_module_index(cls, package_root: Path) -> dict[str, list[str]]:
        """ファイル名ステムからモジュール候補を引けるインデックスを構築する.

        Args:
            package_root: 探索ルートディレクトリ.

        Returns:
            dict[str, list[str]]: ステムをキーにした相対モジュール名一覧.
        """
        module_index: dict[str, list[str]] = defaultdict(list)
        for py_path in package_root.rglob("*.py"):
            if py_path.name.startswith("_"):
                continue
            relative_module = (
                py_path.with_suffix("")
                .relative_to(package_root)
                .as_posix()
                .replace("/", ".")
            )
            module_index[py_path.stem].append(relative_module)

        # 読み込み順を安定化して再現性を担保する。
        return {stem: sorted(module_names) for stem, module_names in module_index.items()}

    @staticmethod
    def _class_name_to_module_stem(class_name: str) -> str:
        """クラス名から推定されるモジュールステムへ変換する."""
        converted = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", class_name)
        converted = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", converted)
        normalized = converted.lower()
        normalized = normalized.replace("postgre_sql", "postgresql")
        normalized = normalized.replace("s_3", "s3")
        return normalized

    @classmethod
    def _resolve_class_from_module(
        cls,
        module_name: str,
        class_name: str,
        base_type: type[Any],
    ) -> type[Any] | None:
        """指定モジュール内から対象クラスを解決する."""
        module = importlib.import_module(module_name, package=cls.__module__)
        target_class = getattr(module, class_name, None)
        if not inspect.isclass(target_class):
            return None
        if not issubclass(target_class, base_type) or target_class is base_type:
            return None
        if target_class.__module__ != module.__name__:
            return None
        return target_class

    @classmethod
    def _load_class_lazy(
        cls,
        class_name: str,
        class_registry: dict[str, type[Any]],
        module_index: dict[str, list[str]],
        package_prefix: str,
        base_type: type[Any],
    ) -> type[Any] | None:
        """クラス名に対応する型を遅延ロードする."""
        cached = class_registry.get(class_name)
        if cached is not None:
            cls._metrics["lazy_hit"] += 1
            return cached

        stem = cls._class_name_to_module_stem(class_name)
        candidate_modules = module_index.get(stem, [])
        for relative_module in candidate_modules:
            class_obj = cls._resolve_class_from_module(
                f"{package_prefix}{relative_module}",
                class_name,
                base_type,
            )
            if class_obj is not None:
                class_registry[class_name] = class_obj
                cls._metrics["lazy_hit"] += 1
                return class_obj
        cls._metrics["lazy_miss"] += 1
        return None

    @classmethod
    def _build_parameter_registry(cls) -> dict[str, type[SubModuleParameter]]:
        """Parameter クラスのレジストリを作成する."""
        package_root = Path(__file__).resolve().parents[1] / "sub_module_parameter"
        package_prefix = "...sub_module_parameter."
        return cls._build_registry(
            package_root=package_root,
            package_prefix=package_prefix,
            base_type=SubModuleParameter,
        )

    @classmethod
    def _build_sub_module_registry(cls) -> dict[str, type[SubModule]]:
        """SubModule クラスのレジストリを作成する."""
        package_root = Path(__file__).resolve().parent
        package_prefix = ".."
        return cls._build_registry(
            package_root=package_root,
            package_prefix=package_prefix,
            base_type=SubModule,
        )

    @classmethod
    def _build_registry(
        cls,
        package_root: Path,
        package_prefix: str,
        base_type: type[Any],
    ) -> dict[str, type[Any]]:
        """指定ディレクトリ配下のクラスレジストリを作成する.

        Args:
            package_root: 探索ルートディレクトリ.
            package_prefix: import 時のパッケージ接頭辞.
            base_type: 対象とする基底クラス.

        Returns:
            dict[str, type]: クラス名をキーにしたレジストリ.
        """
        class_registry: dict[str, type[Any]] = {}
        for py_path in package_root.rglob("*.py"):
            if py_path.name.startswith("_"):
                continue
            relative_module = (
                py_path.with_suffix("")
                .relative_to(package_root)
                .as_posix()
                .replace("/", ".")
            )
            module = importlib.import_module(
                f"{package_prefix}{relative_module}",
                package=cls.__module__,
            )
            for _attr_name, attr in inspect.getmembers(module, inspect.isclass):
                if attr.__module__ != module.__name__:
                    continue
                if issubclass(attr, base_type) and attr is not base_type:
                    class_registry[attr.__name__] = attr
        return class_registry

    @classmethod
    def _get_parameter_class(cls, class_name: str) -> type[SubModuleParameter] | None:
        """Parameter クラスを解決する."""
        cls._ensure_indexes()
        if cls._parameter_module_index is None:
            return None

        resolved = cls._load_class_lazy(
            class_name,
            cls._parameter_class_registry,
            cls._parameter_module_index,
            package_prefix="...sub_module_parameter.",
            base_type=SubModuleParameter,
        )
        if resolved is not None:
            return resolved

        if not cls._parameter_full_scan_done:
            with cls._registry_lock:
                if not cls._parameter_full_scan_done:
                    cls._parameter_class_registry.update(cls._build_parameter_registry())
                    cls._parameter_full_scan_done = True
                    cls._metrics["full_scan_parameter"] += 1
        return cls._parameter_class_registry.get(class_name)

    @classmethod
    def _get_sub_module_class(cls, class_name: str) -> type[SubModule] | None:
        """SubModule クラスを解決する."""
        cls._ensure_indexes()
        if cls._sub_module_module_index is None:
            return None

        resolved = cls._load_class_lazy(
            class_name,
            cls._sub_module_class_registry,
            cls._sub_module_module_index,
            package_prefix="..",
            base_type=SubModule,
        )
        if resolved is not None:
            return resolved

        if not cls._sub_module_full_scan_done:
            with cls._registry_lock:
                if not cls._sub_module_full_scan_done:
                    cls._sub_module_class_registry.update(cls._build_sub_module_registry())
                    cls._sub_module_full_scan_done = True
                    cls._metrics["full_scan_sub_module"] += 1
        return cls._sub_module_class_registry.get(class_name)

    @classmethod
    def reset_registry(cls):
        """テスト時にクラスレジストリを初期化する."""
        cls._parameter_class_registry = {}
        cls._sub_module_class_registry = {}
        cls._parameter_module_index = None
        cls._sub_module_module_index = None
        cls._parameter_full_scan_done = False
        cls._sub_module_full_scan_done = False
        cls.reset_metrics()

    @classmethod
    def metrics(cls) -> dict[str, int]:
        """現在のロード統計を返す."""
        return dict(cls._metrics)

    @classmethod
    def reset_metrics(cls) -> None:
        """ロード統計を初期化する."""
        for key in cls._metrics:
            cls._metrics[key] = 0

    @classmethod
    def create_sub_module(
        cls,
        sub_module_name: str,
        sub_module_parameter_dict: dict[str, Any],
        mode: str | None = None,
        component_resolver: Callable[[str], object] | None = None,
    ) -> SubModule:
        """サブモジュールを1件生成する.

        Args:
            sub_module_name: サブモジュール名.
            sub_module_parameter_dict: パラメータ辞書.
            mode: モード名.
            component_resolver: コンポーネント解決関数.

        Returns:
            SubModule: 生成したサブモジュール.
        """
        sub_module_key = sub_module_name if mode is None else f"{sub_module_name}{mode}"
        sub_module_param_key = f"{sub_module_key}Parameter"

        parameter_class = cls._get_parameter_class(sub_module_param_key)
        if parameter_class is None:
            raise SubModuleLoadError(sub_module_param_key)
        sub_module_parameter = parameter_class(sub_module_parameter_dict)

        sub_module_class = cls._get_sub_module_class(sub_module_key)
        if sub_module_class is None:
            raise SubModuleLoadError(sub_module_key)

        if component_resolver is None:
            return sub_module_class(sub_module_parameter)

        try:
            return sub_module_class(sub_module_parameter, component_resolver=component_resolver)
        except TypeError:
            # 互換のため、旧シグネチャしか受けない実装にも対応する。
            sub_module = sub_module_class(sub_module_parameter)
            if hasattr(sub_module, "set_component_resolver"):
                sub_module.set_component_resolver(component_resolver)
            return sub_module

    @classmethod
    def create_sub_module_list(
        cls,
        sub_module_name: str,
        sub_module_parameter_dict: dict[str, Any],
        mode: str | None = None,
        component_resolver: Callable[[str], object] | None = None,
    ) -> list[SubModule]:
        """サブモジュール配列を生成する.

        Args:
            sub_module_name: サブモジュール名.
            sub_module_parameter_dict: パラメータ辞書.
            mode: モード名.
            component_resolver: コンポーネント解決関数.

        Returns:
            list[SubModule]: 生成したサブモジュール配列.
        """
        return [
            cls.create_sub_module(
                sub_module_name,
                sub_module_parameter_dict,
                mode,
                component_resolver=component_resolver,
            )
        ]
