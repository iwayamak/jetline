# -*- coding: utf-8 -*-

import os.path
import re
import distutils.util
from ..exception.sub_module_parameter_error import SubModuleParameterError
from ..container.container import Container


class Validator(object):

    @staticmethod
    def component_key(func):
        def wrapper(*args, **kwargs):
            key = args[0]
            if len(args) > 1:
                key = args[1]
            if key is None:
                return func(*args, **kwargs)
            try:
                Container.component(key)
            except Exception:
                raise SubModuleParameterError('component_key', key)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def path(func):
        def wrapper(*args, **kwargs):
            path_str = args[0]
            if len(args) > 1:
                path_str = args[1]
            if path_str is None:
                return func(*args, **kwargs)
            if not os.path.exists(path_str):
                raise SubModuleParameterError('file_path', path_str)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def digit(func):
        def wrapper(*args, **kwargs):
            i = args[0]
            if len(args) > 1:
                i = args[1]
            if i is None:
                return func(*args, **kwargs)
            if not isinstance(i, int):
                if not str(i).isdigit():
                    raise SubModuleParameterError('digit', i)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def boolean(func):
        def wrapper(*args, **kwargs):
            b = args[0]
            if len(args) > 1:
                b = args[1]
            if b is None:
                return func(*args, **kwargs)
            if not isinstance(b, bool):
                try:
                    distutils.util.strtobool(b)
                except Exception:
                    raise SubModuleParameterError('boolean', b)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def regexp(pattern):
        def _regexp(func):
            def wrapper(*args, **kwargs):
                v = args[0]
                if len(args) > 1:
                    v = args[1]
                if v is None:
                    return func(*args, **kwargs)
                r = re.search(pattern, str(v), re.MULTILINE)
                if r is None:
                    raise SubModuleParameterError('regexp:' + pattern, v)
                return func(*args, **kwargs)
            return wrapper
        return _regexp

    @staticmethod
    def range(lower, upper):
        def _regexp(func):
            def wrapper(*args, **kwargs):
                v = args[0]
                if len(args) > 1:
                    v = args[1]
                if v is None:
                    return func(*args, **kwargs)
                try:
                    if v < lower or v > upper:
                        raise SubModuleParameterError(f'range [{lower}] to [{upper}]', v)
                except TypeError:
                    raise SubModuleParameterError(f'range [{lower}] to [{upper}]', v)
                return func(*args, **kwargs)
            return wrapper
        return _regexp

    @staticmethod
    def list(func):
        def wrapper(*args, **kwargs):
            v = args[0]
            if len(args) > 1:
                v = args[1]
            if v is None:
                return func(*args, **kwargs)
            if not isinstance(v, list):
                raise SubModuleParameterError('list', v)
            return func(*args, **kwargs)
        return wrapper

    @staticmethod
    def dict(func):
        def wrapper(*args, **kwargs):
            v = args[0]
            if len(args) > 1:
                v = args[1]
            if v is None:
                return func(*args, **kwargs)
            if not isinstance(v, dict):
                raise SubModuleParameterError('dict', v)
            return func(*args, **kwargs)
        return wrapper
