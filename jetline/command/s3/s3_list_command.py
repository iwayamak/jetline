"""S3 オブジェクト一覧取得コマンド。."""

from collections.abc import MutableSequence

from ...container.component.s3_component import S3Component
from .abc.s3_command import S3Command


class S3ListCommand(S3Command):
    """prefix 条件で S3 オブジェクトを列挙する。."""

    def __init__(self, component: S3Component, prefix: str, object_list: MutableSequence):
        """S3 一覧取得コマンドを初期化する。.

        Args:
            component: S3 コンポーネント。
            prefix: 検索 prefix。
            object_list: 結果格納先リスト。
        """
        self._prefix = prefix
        self._object_list = object_list
        super().__init__(component)

    def run(self):
        """S3 オブジェクト一覧を取得する。."""
        super().run()
        summary_iter = self._bucket.objects.filter(Prefix=self._prefix)
        for s3_object in summary_iter:
            self._object_list.append(s3_object)
