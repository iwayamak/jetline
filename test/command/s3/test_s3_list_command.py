"""S3ListCommand のユニットテスト."""

import os

from jetline.command.command_queue import CommandQueue
from jetline.command.local.touch_file_command import TouchFileCommand
from jetline.command.s3.s3_list_command import S3ListCommand
from jetline.command.s3.s3_put_command import S3PutCommand
from jetline.container.container import Container

from ...abc.base_test_case import BaseTestCase

TEST_DATA_PATH_LIST = [
    os.path.join(os.path.dirname(__file__), f"test_s3_list_command_0{i}.csv") for i in range(2)
]


class TestS3ListCommand(BaseTestCase):
    """S3 プレフィックス列挙を検証する."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する."""
        self._component = Container().component("S3_COMPONENT.ID=UT")
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        """列挙対象オブジェクトを S3 に配置する."""
        queue = CommandQueue()
        for test_data_path in TEST_DATA_PATH_LIST:
            queue.add_command(TouchFileCommand(test_data_path))
            queue.add_command(
                S3PutCommand(
                    Container().component("S3_COMPONENT.ID=UT"),
                    test_data_path,
                    f"test_s3_list_command/{os.path.basename(test_data_path)}",
                )
            )
        queue.execute()

    def test_s3_list(self) -> None:
        """指定プレフィックスで期待オブジェクト一覧を取得できることを確認する."""
        object_list = []
        S3ListCommand(self._component, "test_s3_list_command", object_list).execute()

        for index, test_data_path in enumerate(TEST_DATA_PATH_LIST):
            self.assertEqual(
                object_list[index].key,
                f"test_s3_list_command/{os.path.basename(test_data_path)}",
            )
        self.assertEqual(len(object_list), len(TEST_DATA_PATH_LIST))
