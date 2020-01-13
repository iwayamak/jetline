# -*- coding: utf-8 -*-

from .template_string import TemplateString
from dateutil import relativedelta
from datetime import datetime
from ...exception.template_string.undefined_body_string_error import UndefinedBodyStringError


class TimestampString(TemplateString):

    SUB_STR = 'timestamp'

    def __init__(self):
        super().__init__()

    def evaluate(self):
        if self._option is None:
            target_date = datetime.now()
        else:
            index = self._option.index('=')
            key = self._option[0:index]
            value = self._option[index + 1:]
            if key == 'years':
                target_date = datetime.now() + relativedelta.relativedelta(years=int(value))
            elif key == 'months':
                target_date = datetime.now() + relativedelta.relativedelta(months=int(value))
            elif key == 'days':
                target_date = datetime.now() + relativedelta.relativedelta(days=int(value))
            elif key == 'hours':
                target_date = datetime.now() + relativedelta.relativedelta(hours=int(value))
            elif key == 'minutes':
                target_date = datetime.now() + relativedelta.relativedelta(minutes=int(value))
            elif key == 'seconds':
                target_date = datetime.now() + relativedelta.relativedelta(seconds=int(value))
            else:
                raise UndefinedBodyStringError('timestamp(' + self._option + ')')
        if self._str_format is None:
            self._result = target_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._result = target_date.strftime(self._str_format)
        super().evaluate()
