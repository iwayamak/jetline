# -*- coding: utf-8 -*-

import os
import sys
import logging.config
from jetline.module.module import Module
from jetline.util.path_util import PathUtil
from jetline.util.yaml_util import YamlUtil
from jetline.share_parameter.share_parameter import ShareParameter


if __name__ == '__main__':
    exit_code = ShareParameter.error_return_code
    module = None
    logger = None
    try:
        exec_yaml_path, exec_date, working_dir = Module.parse_kick_args(sys.argv[1:])
        if working_dir is not None:
            os.chdir(working_dir)
        batch_name, ext = os.path.splitext(os.path.basename(exec_yaml_path))
        ShareParameter.batch_name = batch_name
        logging.config.dictConfig(YamlUtil.load_file(PathUtil.logging_conf_path()))
        logger = logging.getLogger('jetline')
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
        if logger is not None:
            logger.info(f'module finished... exit_code: {str(exit_code)}')
            sys.exit(exit_code)
