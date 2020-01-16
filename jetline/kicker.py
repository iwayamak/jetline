# -*- coding: utf-8 -*-

import os
import sys
import logging.config
from .module.module import Module
from .util.path_util import PathUtil
from .util.yaml_util import YamlUtil
from .share_parameter.share_parameter import ShareParameter

logging.config.dictConfig(YamlUtil.load_file(PathUtil.logging_conf_path()))
logger = logging.getLogger('jetline')

if __name__ == '__main__':
    exit_code = ShareParameter.error_return_code
    module = None
    try:
        exec_yaml_path, exec_date = Module.parse_kick_args(sys.argv[1:])
        batch_name, ext = os.path.splitext(os.path.basename(exec_yaml_path))
        ShareParameter.batch_name = batch_name

        logger.info('module kicked...')
        logger.info('exec yaml: ' + exec_yaml_path)
        logger.info('exec_date: ' + exec_date)
        module = Module(exec_yaml_path, exec_date)
        module.set_up()
        module.execute()
        exit_code = ShareParameter.success_return_code
    except Exception as e:
        logger.exception(e)
        exit_code = ShareParameter.error_return_code
    finally:
        if module is not None:
            module.tear_down()
        logger.info('module finished... exit_code: ' + str(exit_code))
        sys.exit(exit_code)
