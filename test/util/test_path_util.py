"""PathUtil のユニットテスト。."""

import os

from jetline.util.path_util import PathUtil
from test.abc.base_test_case import BaseTestCase


class TestPathUtil(BaseTestCase):
    """PathUtil の各パス解決を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_framework_root_path(self):
        """プロジェクトルートが存在することを確認する。."""
        jetline_root_path = PathUtil.jetline_root_path()
        self.assertTrue(os.path.exists(jetline_root_path))

    def test_settings_root_path(self):
        """設定ディレクトリが存在することを確認する。."""
        settings_root_path = PathUtil.settings_root_path()
        self.assertTrue(os.path.exists(settings_root_path))

    def test_all_component_yaml_path(self):
        """コンポーネント設定ディレクトリが存在することを確認する。."""
        component_path = PathUtil.component_path()
        self.assertTrue(os.path.exists(component_path))

    def test_logger_yaml_path(self):
        """ログ設定ファイルが存在することを確認する。."""
        logging_conf_path = PathUtil.logging_conf_path()
        self.assertTrue(os.path.exists(logging_conf_path))
