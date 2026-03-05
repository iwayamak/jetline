"""S3 一覧取得サブモジュール。"""

import logging

import dateutil.tz as tz

from ...sub_module_parameter.s3.s3_list_parameter import S3ListParameter
from .abc.s3_sub_module import S3SubModule

logger = logging.getLogger('jetline')


class S3List(S3SubModule):
    """S3 から条件一致オブジェクトを一覧化する。"""

    def __init__(self, param: S3ListParameter):
        """S3一覧取得サブモジュールを初期化する。

        Args:
            param: S3一覧取得パラメータ。
        """
        super().__init__(param)

    def run(self):
        """サブモジュール処理を実行する。"""
        s3_file_pattern = self._parameter.s3_file_path.get()
        self._result_s3_file_list = self.list_objects_by_pattern(s3_file_pattern)
        for result_s3_file in self._result_s3_file_list:
            last_modified = result_s3_file.last_modified.astimezone(tz.tzlocal()).strftime(
                '%Y-%m-%d %H:%M:%S'
            )
            size = str(result_s3_file.size).rjust(13)
            logger.info(f'{last_modified} {size} Bytes {result_s3_file.key}')
