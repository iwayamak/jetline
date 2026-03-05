"""SubModuleCreator のユニットテスト。."""

import os

from jetline.module.sub_module.db.postgresql.postgresql_processing import PostgreSQLProcessing
from jetline.module.sub_module.db.postgresql.postgresql_processing_count import (
    PostgreSQLProcessingCount,
)
from jetline.module.sub_module.sub_module_creator import SubModuleCreator
from jetline.module.sub_module_parameter.db.postgresql import (
    postgresql_processing_count_parameter,
    postgresql_processing_parameter,
)
from test.abc.base_test_case import BaseTestCase


class TestSubModuleCreator(BaseTestCase):
    """SubModuleCreator の生成ロジックを検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._sql_file_name = os.path.join(
            os.path.dirname(__file__),
            "test_sub_module_creator.sql",
        )
        super().__init__(*args, **kwargs)

    def test_create_sub_module(self):
        """Mode なしで通常サブモジュールを生成できることを確認する。."""
        sub_module = SubModuleCreator.create_sub_module(
            "PostgreSQLProcessing",
            {
                "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=TEST_COMPONENT",
                "sql_file_name": self._sql_file_name,
            },
        )

        self.assertIsInstance(sub_module, PostgreSQLProcessing)
        self.assertIsInstance(
            sub_module._parameter,
            postgresql_processing_parameter.PostgreSQLProcessingParameter,
        )

    def test_create_sub_module_set_mode(self):
        """Mode 指定で派生サブモジュールを生成できることを確認する。."""
        sub_module = SubModuleCreator.create_sub_module(
            "PostgreSQLProcessing",
            {
                "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=TEST_COMPONENT",
                "sql_file_name": self._sql_file_name,
                "assert_eq": 3,
            },
            "Count",
        )

        self.assertIsInstance(sub_module, PostgreSQLProcessingCount)
        self.assertIsInstance(
            sub_module._parameter,
            postgresql_processing_count_parameter.PostgreSQLProcessingCountParameter,
        )

    def test_create_sub_module_list(self):
        """create_sub_module_list が1件配列を返すことを確認する。."""
        sub_module_list = SubModuleCreator.create_sub_module_list(
            "PostgreSQLProcessing",
            {
                "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=TEST_COMPONENT",
                "sql_file_name": self._sql_file_name,
            },
        )

        self.assertEqual(1, len(sub_module_list))
        self.assertIsInstance(sub_module_list[0], PostgreSQLProcessing)
        self.assertIsInstance(
            sub_module_list[0]._parameter,
            postgresql_processing_parameter.PostgreSQLProcessingParameter,
        )

    def test_create_sub_module_list_set_mode(self):
        """Mode 指定時の create_sub_module_list 結果を確認する。."""
        sub_module_list = SubModuleCreator.create_sub_module_list(
            "PostgreSQLProcessing",
            {
                "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=TEST_COMPONENT",
                "sql_file_name": self._sql_file_name,
                "assert_eq": 3,
            },
            "Count",
        )

        self.assertEqual(1, len(sub_module_list))
        self.assertIsInstance(sub_module_list[0], PostgreSQLProcessingCount)
        self.assertIsInstance(
            sub_module_list[0]._parameter,
            postgresql_processing_count_parameter.PostgreSQLProcessingCountParameter,
        )
