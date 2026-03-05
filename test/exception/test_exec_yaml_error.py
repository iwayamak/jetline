"""ExecYamlError のユニットテスト。."""

from jetline.exception.exec_yaml_error import ExecYamlError
from test.abc.base_test_case import BaseTestCase


class TestExecYamlError(BaseTestCase):
    """ExecYamlError の送出を確認する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_raise(self):
        """ExecYamlError が送出できることを確認する。."""
        with self.assertRaises(ExecYamlError):
            raise ExecYamlError("exec yaml error")
