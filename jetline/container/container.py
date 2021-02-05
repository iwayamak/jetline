# -*- coding: utf-8 -*-

import os
import threading
import importlib
import importlib.util
from ..util.yaml_util import YamlUtil
from ..util.path_util import PathUtil
from ..exception.component_load_error import ComponentLoadError


class Container(object):

    _all_component_param = None
    _component = None
    __singleton_lock = threading.Lock()
    KEY_CLASS = 'class'
    METHOD_CREATE_COMPONENT = 'create_component'

    @classmethod
    def init_load(cls):
        cls._all_component_param = YamlUtil.load_dir(PathUtil.component_path())
        cls._component = {}

    @classmethod
    def component(cls, key):
        if not cls._all_component_param or not cls._component:
            with cls.__singleton_lock:
                if not cls._all_component_param or not cls._component:
                    cls.init_load()
        if key not in cls._component:
            component_class = cls._all_component_param[key][cls.KEY_CLASS]
            d = os.path.join(os.path.dirname(__file__), 'component')
            files = os.listdir(d)
            obj = None
            for file in files:
                if file.startswith('_') or not file.endswith('.py'):
                    continue
                name = file[:-3]
                m = importlib.import_module(
                    '..component.' + name, package=cls.__module__
                )
                obj_list = dir(m)
                if component_class in obj_list:
                    obj = getattr(m, component_class)
                    break
            if obj is None:
                raise ComponentLoadError(component_class)
            component_instance = \
                getattr(obj, cls.METHOD_CREATE_COMPONENT)(cls._all_component_param[key])
            cls._component[key] = component_instance
        return cls._component[key]
