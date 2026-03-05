"""S3PutParameter のユニットテスト。."""

from jetline.exception.sub_module_parameter_error import SubModuleParameterError
from jetline.module.sub_module_parameter.s3.s3_put_parameter import S3PutParameter
from test.abc.base_test_case import BaseTestCase


class TestS3PutParameter(BaseTestCase):
    """S3PutParameter の入力検証を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_all_parameter(self):
        """全パラメータを指定した場合に値が保持されることを確認する。."""
        param = S3PutParameter(
            {
                "s3_component_key": "S3_COMPONENT.ID=UT",
                "local_file_path": "test_source.csv",
                "s3_dir_path": "test_dir",
                "end_file_name": "endfile",
            }
        )

        self.assertEqual("S3_COMPONENT.ID=UT", param.s3_component_key.get())
        self.assertEqual("test_source.csv", param.local_file_path.get())
        self.assertEqual("test_dir", param.s3_dir_path.get())
        self.assertEqual("endfile", param.end_file_name.get())

    def test_component_key_path_not_set(self):
        """コンポーネントキー未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter({"local_file_path": "test_source.csv", "s3_dir_path": "test_dir"})

    def test_s3_dir_path_not_set(self):
        """S3 送信先未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter(
                {"s3_component_key": "S3_COMPONENT.ID=UT", "local_file_path": "test_source.csv"}
            )

    def test_local_file_path_not_set(self):
        """ローカルファイルパス未指定で例外となることを確認する。."""
        with self.assertRaises(SubModuleParameterError):
            S3PutParameter({"s3_component_key": "S3_COMPONENT.ID=UT", "s3_dir_path": "test_dir"})
