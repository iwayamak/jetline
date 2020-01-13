# -*- coding: utf-8 -*-

import os
import unittest
from ...util.path_util import PathUtil


class TestPathUtil(unittest.TestCase):

    def test_framework_root_path(self):
        framework_root_path = PathUtil.framework_root_path()
        self.assertTrue(os.path.exists(framework_root_path))

    def test_settings_root_path(self):
        settings_root_path = PathUtil.settings_root_path()
        self.assertTrue(os.path.exists(settings_root_path))

    def test_all_component_yaml_path(self):
        component_path = PathUtil.component_path()
        self.assertTrue(os.path.exists(component_path))

    def test_logger_yaml_path(self):
        logging_conf_path = PathUtil.logging_conf_path()
        self.assertTrue(os.path.exists(logging_conf_path))
