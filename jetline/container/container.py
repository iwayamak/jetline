
"""コンポーネント設定の読み込みとインスタンス生成を担うコンテナ。."""

import importlib
import os
import threading

from ..exception.component_load_error import ComponentLoadError
from ..util.path_util import PathUtil
from ..util.yaml_util import YamlUtil


class Container:
    """YAML で定義したコンポーネントを遅延生成・キャッシュする。."""

    _all_component_param = None
    _component = None
    _component_class_map = None
    __singleton_lock = threading.Lock()
    KEY_CLASS = 'class'
    METHOD_CREATE_COMPONENT = 'create_component'

    @classmethod
    def init_load(cls):
        """設定ファイルを読み込み、内部キャッシュを初期化する。."""
        cls._all_component_param = YamlUtil.load_dir(PathUtil.component_path())
        cls._component = {}
        cls._component_class_map = cls._load_component_class_map()

    @classmethod
    def _load_component_class_map(cls):
        """利用可能なコンポーネントクラスを走査してマップ化する。.

        Returns:
            dict[str, type]: クラス名をキーにしたクラスマップ。
        """
        component_class_map = {}
        component_module_dir = os.path.join(os.path.dirname(__file__), 'component')
        for filename in os.listdir(component_module_dir):
            if filename.startswith('_') or not filename.endswith('.py'):
                continue
            module_name = filename[:-3]
            module = importlib.import_module(
                '..component.' + module_name, package=cls.__module__
            )
            for attribute_name in dir(module):
                attr = getattr(module, attribute_name)
                if isinstance(attr, type) and hasattr(attr, cls.METHOD_CREATE_COMPONENT):
                    component_class_map[attribute_name] = attr
        return component_class_map

    @classmethod
    def reset(cls):
        """コンテナ内部キャッシュを初期化する。."""
        cls._all_component_param = None
        cls._component = None
        cls._component_class_map = None

    @classmethod
    def component(cls, key):
        """コンポーネントを取得する。.

        Args:
            key: コンポーネントキー。

        Returns:
            object: コンポーネントインスタンス。
        """
        if cls._all_component_param is None or cls._component is None:
            with cls.__singleton_lock:
                if cls._all_component_param is None or cls._component is None:
                    cls.init_load()

        if key not in cls._component:
            if key not in cls._all_component_param:
                raise KeyError(f'component key not found: {key}')

            component_class = cls._all_component_param[key][cls.KEY_CLASS]
            component_type = cls._component_class_map.get(component_class)
            if component_type is None:
                raise ComponentLoadError(component_class)

            component_instance = getattr(
                component_type, cls.METHOD_CREATE_COMPONENT
            )(cls._all_component_param[key])
            cls._component[key] = component_instance
        return cls._component[key]
