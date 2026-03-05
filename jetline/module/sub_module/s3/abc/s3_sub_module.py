"""S3 サブモジュールの共通基底。"""

import fnmatch
import logging
import re
from collections.abc import Sequence

from .....command.s3.s3_list_command import S3ListCommand
from ...abc.sub_module import SubModule

logger = logging.getLogger("jetline")


class S3SubModule(SubModule):
    """S3 系サブモジュールの共通処理を提供する基底クラス。"""

    def set_up(self):
        """実行前処理として共通コンテキストをログ出力する。"""
        super().set_up()
        logger.info(
            "Executing %s (component_key=%s)",
            self.__class__.__name__,
            self._parameter.s3_component_key.get(),
        )

    def resolve_s3_component(self):
        """パラメータのコンポーネントキーから S3 コンポーネントを解決する。"""
        return self.resolve_component(self._parameter.s3_component_key.get())

    @staticmethod
    def _extract_prefix_from_pattern(pattern: str) -> str:
        """S3 パターンから効率的な prefix を抽出する。

        Args:
            pattern: `*` や `?` を含む S3 キーパターン。

        Returns:
            str: 最初のワイルドカードまでの prefix。
        """
        wildcard_match = re.search(r"[\*\?\[]", pattern)
        if wildcard_match is None:
            return pattern
        return pattern[: wildcard_match.start()]

    def list_objects_by_pattern(self, pattern: str) -> list:
        """パターン一致する S3 オブジェクト一覧を取得する。

        Args:
            pattern: 取得対象の S3 キーパターン。

        Returns:
            list: パターン一致した S3 オブジェクト一覧。
        """
        component = self.resolve_s3_component()
        object_list: list = []
        prefix = self._extract_prefix_from_pattern(pattern)
        S3ListCommand(component, prefix, object_list).execute()
        return [obj for obj in object_list if fnmatch.fnmatch(obj.key, pattern)]

    @staticmethod
    def extract_keys(objects: Sequence) -> list[str]:
        """S3 オブジェクト列からキー文字列を抽出する。

        Args:
            objects: S3 オブジェクト列。

        Returns:
            list[str]: キー文字列一覧。
        """
        return [obj.key for obj in objects]
