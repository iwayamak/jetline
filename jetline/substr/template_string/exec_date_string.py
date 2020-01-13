# -*- coding: utf-8 -*-

from .template_string import TemplateString
from ...share_parameter.share_parameter import ShareParameter
from dateutil import relativedelta
from ...exception.template_string.undefined_body_string_error import UndefinedBodyStringError


class ExecDateString(TemplateString):

    SUB_STR = 'exec_date'

    def __init__(self):
        super().__init__()

    def evaluate(self):
        if self._option is None:
            target_date = ShareParameter.exec_date
        else:
            index = self._option.index('=')
            key = self._option[0:index]
            value = self._option[index + 1:]
            if key == 'years':
                target_date = ShareParameter.exec_date + relativedelta.relativedelta(years=int(value))
            elif key == 'months':
                target_date = ShareParameter.exec_date + relativedelta.relativedelta(months=int(value))
            elif key == 'days':
                target_date = ShareParameter.exec_date + relativedelta.relativedelta(days=int(value))
            else:
                raise UndefinedBodyStringError('exec_date(' + self._option + ')')
        if self._str_format is None:
            self._result = target_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._result = target_date.strftime(self._str_format)
        super().evaluate()
