"""YamlUtil のユニットテスト。."""

import os

from jetline.util.yaml_util import YamlUtil
from test.abc.base_test_case import BaseTestCase


class TestYamlUtil(BaseTestCase):
    """YamlUtil の読み書き処理を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
        super().__init__(*args, **kwargs)

    def test_load_file(self):
        """単一 YAML ファイルの読込結果を確認する。."""
        yaml_name = os.path.join(self._test_data_dir, "test_yaml_util.yaml")
        data = YamlUtil.load_file(yaml_name)
        sub_module = data["sub_module"][0]

        self.assertEqual(sub_module["name"], "PostgreSQLProcessing")
        self.assertEqual(
            sub_module["param"]["postgresql_component_key"],
            "POSTGRESQL_COMPONENT.ID=UT",
        )
        self.assertEqual(sub_module["param"]["sql_file_name"], "test_postgresql_processing.sql")

    def test_load_dir(self):
        """ディレクトリ内 YAML のマージ結果を確認する。."""
        data = YamlUtil.load_dir(self._test_data_dir)
        sub_module = data["sub_module"][0]

        self.assertEqual(sub_module["name"], "PostgreSQLProcessing")
        self.assertEqual(
            sub_module["param"]["postgresql_component_key"],
            "POSTGRESQL_COMPONENT.ID=UT",
        )
        self.assertEqual(sub_module["param"]["sql_file_name"], "test_postgresql_processing.sql")
        self.assertEqual(data["name"], "test_write_file")
        self.assertEqual(data["value"][0]["param1"], "value1")
        self.assertEqual(data["value"][1]["param2"], "value2")

    def test_write_file(self):
        """辞書を書き出した YAML を再読込できることを確認する。."""
        yaml_name = os.path.join(self._test_data_dir, "test_yaml_util_write.yaml")
        expected = {
            "name": "test_write_file",
            "value": [{"param1": "value1"}, {"param2": "value2"}],
        }
        YamlUtil.write_file(yaml_name, expected)

        actual = YamlUtil.load_file(yaml_name)
        self.assertEqual(actual["name"], "test_write_file")
        self.assertEqual(actual["value"][0]["param1"], "value1")
        self.assertEqual(actual["value"][1]["param2"], "value2")
