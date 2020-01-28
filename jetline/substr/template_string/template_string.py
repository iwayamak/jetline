# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from ...share_parameter.share_parameter import ShareParameter


class TemplateString(object):

    @classmethod
    def exec_date(cls,
                  format_str: str = '%Y%m%d',
                  years: float = None,
                  months: float = None,
                  days: float = None) -> str:
        exec_date = \
            datetime.strptime(
                ShareParameter.exec_date, '%Y%m%d'
            )
        if years is not None:
            exec_date = exec_date + relativedelta(years=years)
        if months is not None:
            exec_date = exec_date + relativedelta(months=months)
        if days is not None:
            exec_date = exec_date + relativedelta(days=days)
        result = exec_date.strftime(format_str)
        return result

    @classmethod
    def timestamp(cls,
                  format_str: str = '%Y%m%d',
                  years: float = None,
                  months: float = None,
                  days: float = None) -> str:
        timestamp = datetime.now()
        if years is not None:
            timestamp = timestamp + relativedelta(years=years)
        if months is not None:
            timestamp = timestamp + relativedelta(months=months)
        if days is not None:
            timestamp = timestamp + relativedelta(days=days)
        result = timestamp.strftime(format_str)
        return result
