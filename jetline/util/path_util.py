# -*- coding: utf-8 -*-

import os


class PathUtil(object):

    SETTINGS_DIR = 'settings'
    COMPONENT_DIR = 'component'
    LOGGING_CONF = 'logging_config.yaml'

    @classmethod
    def jetline_root_path(cls):
        return os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]

    @classmethod
    def settings_root_path(cls):
        path = os.path.split(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )[0]
        return os.path.join(path, cls.SETTINGS_DIR)

    @classmethod
    def component_path(cls):
        return os.path.join(cls.settings_root_path(),  cls.COMPONENT_DIR)

    @classmethod
    def logging_conf_path(cls):
        return os.path.join(cls.settings_root_path(), cls.LOGGING_CONF)

    @classmethod
    def mkdir_if_not_exists(cls, path):
        dir_path = os.path.dirname(path) if os.path.isfile(path) else path
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
