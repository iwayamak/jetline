"""PostgreSQLProcessingParameter のユニットテスト。."""

import os

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.db.postgresql.postgresql_processing_parameter import (
    PostgreSQLProcessingParameter,
)
from test.abc.base_test_case import BaseTestCase


class TestPostgreSQLProcessingParameter(BaseTestCase):
    """SQL 実行パラメータの検証テスト。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        self._sql_file_name = os.path.join(
            os.path.dirname(__file__),
            "sql",
            "test_postgresql_processing.sql",
        )
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """必須パラメータ指定時に値が保持されることを確認する。."""
        param = PostgreSQLProcessingParameter(
            {
                "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=UT",
                "sql_file_name": self._sql_file_name,
            }
        )

        self.assertEqual("POSTGRESQL_COMPONENT.ID=UT", param.postgresql_component_key.get())
        self.assertEqual(self._sql_file_name, param.sql_file_name.get())

    def test_component_key_not_set(self):
        """コンポーネントキー未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter({"sql_file_name": self._sql_file_name})

    def test_sql_filename_not_set(self):
        """SQL ファイル未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter(
                {"postgresql_component_key": "POSTGRESQL_COMPONENT.ID=UT"}
            )

    def test_sql_file_not_exists(self):
        """存在しない SQL ファイル指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            PostgreSQLProcessingParameter(
                {
                    "postgresql_component_key": "POSTGRESQL_COMPONENT.ID=UT",
                    "sql_file_name": "not_exists.sql",
                }
            )
