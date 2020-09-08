# -*- coding: utf-8 -*-

import logging
from retry import retry
from ..parser.kicker_args_parser import KickerArgsParser
from ..util.yaml_util import YamlUtil
from ..share_parameter.share_parameter import ShareParameter
from ..module.sub_module.result.sub_module_result import SubModuleResult
from ..module.sub_module.sub_module_creator import SubModuleCreator
from ..config.config import Config

logger = logging.getLogger('jetline')
tries = 0
delay = 0
backoff = 0
jitter = None
max_delay = 0


class Module(object):
    KEY_SUB_MODULE = 'sub_module'
    KEY_SUB_MODULE_NAME = 'name'
    KEY_SUB_MODULE_PARAM = 'param'
    KEY_SUB_MODULE_MODE = 'mode'

    def __init__(self, exec_yaml_path: str, exec_date: str):
        ShareParameter.exec_yaml_path = exec_yaml_path
        ShareParameter.exec_date = exec_date
        ShareParameter.exec_yaml = YamlUtil.load_file(exec_yaml_path)
        self._sub_module_obj_list = []

    def set_up(self):
        ShareParameter.sub_module_result = SubModuleResult()
        sub_module_list = ShareParameter.exec_yaml[self.KEY_SUB_MODULE]
        for sub_module in sub_module_list:
            sub_module_name = sub_module[self.KEY_SUB_MODULE_NAME]
            if sub_module_name not in Config.AVAILABLE_SUB_MODULE:
                raise Exception(
                    f'this sub_module using is forbidden : {sub_module_name}'
                )
            sub_module_obj_list = \
                SubModuleCreator.create_sub_module_list(
                    sub_module_name,
                    sub_module[self.KEY_SUB_MODULE_PARAM],
                    sub_module[self.KEY_SUB_MODULE_MODE]
                )
            if len(sub_module_obj_list) == 0:
                raise Exception(
                    f'sub_module failed: {sub_module_name}'
                )
            for sub_module_obj in sub_module_obj_list:
                self._sub_module_obj_list.append(sub_module_obj)

    def execute(self):
        ShareParameter.tries_count = 0

        @retry(tries=tries, delay=delay, backoff=backoff, jitter=jitter, max_delay=max_delay, logger=logging)
        def _execute():
            ShareParameter.tries_count += 1
            if ShareParameter.tries_count > 1:
                logger.info(f'Try count is {ShareParameter.tries_count}')
            for seq, sub_module_obj in enumerate(self._sub_module_obj_list):
                logger.info(f'seq {seq + 1}: {type(sub_module_obj).__name__}')
                sub_module_obj.execute()

        _execute()

    def tear_down(self):
        pass

    @classmethod
    def parse_kick_args(cls, argv):
        k = KickerArgsParser(argv)
        ShareParameter.dry_run_mode = k.dry_run()
        globals().update({'tries': k.tries()})
        globals().update({'delay': k.delay()})
        globals().update({'backoff': k.backoff()})
        globals().update({'jitter': k.jitter()})
        globals().update({'max_delay': k.max_delay()})
        return k.exec_yaml_path(), k.exec_date(), k.working_dir()
