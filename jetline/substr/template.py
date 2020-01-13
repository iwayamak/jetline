# -*- coding: utf-8 -*-

import re
import logging
from ..exception.template_string.body_string_error import BodyStringError
from ..exception.template_string.undefined_body_string_error import UndefinedBodyStringError
from .template_string.exec_date_string import ExecDateString
from .template_string.timestamp_string import TimestampString
from .template_string.log_dir_string import LogDirString
from .template_string.batch_name_string import BatchNameString

logger = logging.getLogger('jetline')


class Template(object):

    PATTERN = r'\$\{[_\-a-zA-Z0-9\.\(\):%/\x20=]*\}'
    BODY_START_INDEX = 2
    BODY_END_INDEX = -1
    SUB_STR_MIN_LENGTH = 4

    SUB_STRINGS = {
        ExecDateString.SUB_STR: ExecDateString(),
        TimestampString.SUB_STR: TimestampString(),
        LogDirString.SUB_STR: LogDirString(),
        BatchNameString.SUB_STR: BatchNameString(),
    }

    def __init__(self, src_str, query_mode=True):
        self._src_str = src_str
        self._query_mode = query_mode

    def apply(self):
        result_str = self._src_str
        p = re.compile(self.PATTERN)
        ls = p.findall(self._src_str)
        logger.debug('extract target: ' + str(ls))
        done_ls = []
        for s in ls:
            if s not in done_ls:
                evaluated_str = self._evaluate(s)
                result_str = result_str.replace(s, evaluated_str)
                done_ls.append(s)
        return result_str

    def _extract_body_str(self, target_str):
        if len(target_str) < self.SUB_STR_MIN_LENGTH:
            return None
        return target_str[self.BODY_START_INDEX:self.BODY_END_INDEX]

    def _evaluate(self, target_str):
        body_str = self._extract_body_str(target_str)
        if body_str is None:
            raise BodyStringError(body_str)
        if '.' in body_str:
            raise BodyStringError(body_str)
        else:
            if ':' in body_str:
                index = body_str.find(':')
                if index == 0:
                    raise UndefinedBodyStringError(body_str)
                body_str_key = body_str[0:index]
                body_str_format = body_str[index + 1:]
            else:
                body_str_key = body_str
                body_str_format = None

            # option
            if body_str_key.count('(') == 1 and body_str_key[-1] == ')':
                index = body_str_key.find('(')
                if index == 0:
                    raise UndefinedBodyStringError(body_str_key)
                body_str_option = body_str_key[index + 1:-1]
                body_str_key = body_str_key[0:index]
            else:
                body_str_option = None

            if body_str_key in self.SUB_STRINGS.keys():
                template_string = self.SUB_STRINGS[body_str_key]
                template_string._str_format = body_str_format
                template_string._option = body_str_option
                template_string.query_mode = self._query_mode
                del template_string.result
                return template_string.result
            else:
                raise UndefinedBodyStringError(body_str)
