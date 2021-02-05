# -*- coding: utf-8 -*-

from ...exception.sub_module_load_error import SubModuleLoadError
import os
import glob
import importlib
import importlib.util


class SubModuleCreator(object):

    @classmethod
    def create_sub_module(cls,
                          sub_module_name: str,
                          sub_module_parameter_dict: {str: str},
                          mode=None):
        sub_module_key = sub_module_name
        if mode is not None:
            sub_module_key = f'{sub_module_name}{mode}'
        sub_module_param_key = f'{sub_module_key}Parameter'
        sub_module_param_dir = \
            os.path.join(
                os.path.dirname(__file__), os.pardir, 'sub_module_parameter'
            )
        sub_module_param_files = \
            glob.glob(
                os.path.join(sub_module_param_dir, '**/*.py'), recursive=True
            )
        sub_module_parameter = None
        for sub_module_param_file in sub_module_param_files:
            if os.path.basename(sub_module_param_file).startswith('_'):
                continue
            module_name = \
                os.path.splitext(sub_module_param_file)[0].replace(
                    f'{sub_module_param_dir}{os.path.sep}', ''
                ).replace(
                    os.path.sep, '.'
                )
            module = importlib.import_module(f'...sub_module_parameter.{module_name}', package=cls.__module__)
            obj_list = dir(module)
            if sub_module_param_key in obj_list:
                sub_module_parameter = getattr(module, sub_module_param_key)(sub_module_parameter_dict)
                break

        if sub_module_parameter is None:
            raise SubModuleLoadError(sub_module_param_key)

        sub_module_dir = os.path.dirname(__file__)
        sub_module_files = \
            glob.glob(
                os.path.join(sub_module_dir, '**/*.py'), recursive=True
            )
        sub_module = None
        for sub_module_file in sub_module_files:
            if os.path.basename(sub_module_file).startswith('_'):
                continue
            module_name = \
                os.path.splitext(sub_module_file)[0].replace(
                    f'{sub_module_dir}{os.path.sep}', ''
                ).replace(
                    os.path.sep, '.'
                )
            module = importlib.import_module(f'..{module_name}', package=cls.__module__)
            obj_list = dir(module)

            # create the sub_module with an arg of the sub_module_parameter
            if sub_module_key in obj_list:
                sub_module = getattr(module, sub_module_key)(sub_module_parameter)
                break

        if sub_module is None:
            raise SubModuleLoadError(sub_module_key)

        return sub_module

    @classmethod
    def create_sub_module_list(cls,
                               sub_module_name: str,
                               sub_module_parameter_dict: {str: str},
                               mode=None):
        sub_module_list = [
            cls.create_sub_module(
                sub_module_name, sub_module_parameter_dict, mode
            )
        ]
        return sub_module_list
