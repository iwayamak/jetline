"""テスト共通基底クラス。."""

import logging.config
import unittest

from jetline.share_parameter.share_parameter import ShareParameter
from jetline.util.path_util import PathUtil
from jetline.util.yaml_util import YamlUtil


class BaseTestCase(unittest.TestCase):
    """全テストで使う共通初期化を提供する。."""

    def __init__(self, *args, **kwargs):
        """ロガー初期化と実行コンテキスト初期化を行う。.

        Args:
            *args: unittest.TestCase の位置引数。
            **kwargs: unittest.TestCase のキーワード引数。
        """
        ShareParameter.reset()
        PathUtil.mkdir_if_not_exists(PathUtil.logs_path())
        ShareParameter.batch_name = self.__class__.__name__
        logging.config.dictConfig(YamlUtil.load_file(PathUtil.logging_conf_path()))
        logger = logging.getLogger('jetline')
        logger.info('start')
        super().__init__(*args, **kwargs)
