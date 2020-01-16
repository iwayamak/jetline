# -*- coding: utf-8 -*-

import time
from typing import List, Union
from datetime import datetime
from dateutil import relativedelta


class TimeUtil(object):

    @classmethod
    def current_yyyymmddhhmiss(cls) -> str:
        return datetime.now().strftime('%Y%m%d%H%M%S')

    @classmethod
    def current_yyyymmdd(cls) -> str:
        return datetime.now().strftime('%Y%m%d')

    @classmethod
    def datetime_object_from_yyyymmdd_str(cls, tstr: str) -> datetime:
        return datetime.strptime(tstr, '%Y%m%d')

    @classmethod
    def yyyymmdd_str(cls, dt: datetime) -> str:
        return dt.strftime('%Y%m%d')

    @classmethod
    def datetime_list(cls, fr_str_yyyymmdd: str,
                      to_str_yyyymmdd: Union[str, None]) -> List[datetime]:
        dt_lst = []
        if to_str_yyyymmdd is None:
            dt_lst.append(
                TimeUtil.datetime_object_from_yyyymmdd_str(
                    fr_str_yyyymmdd
                )
            )
        else:
            target_date_str = fr_str_yyyymmdd
            while True:
                target_date = \
                    TimeUtil.datetime_object_from_yyyymmdd_str(
                        target_date_str
                    )
                dt_lst.append(target_date)
                if target_date_str == to_str_yyyymmdd:
                    break
                target_date_str = \
                    TimeUtil.yyyymmdd_str(
                        target_date + relativedelta.relativedelta(days=1)
                    )
        return list(dt_lst)

    @classmethod
    def get_unix_time(cls, target_date: datetime) -> int:
        return int(time.mktime(target_date.timetuple()))

    @classmethod
    def datetime_delta(cls, target_date: datetime, years: int = 0, months: int = 0, days: int = 0, leapdays: int = 0,
                       weeks: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0,
                       microseconds: int = 0) -> datetime:
        return target_date + relativedelta.relativedelta(years=years, months=months, days=days, leapdays=leapdays,
                                                         weeks=weeks, hours=hours, minutes=minutes, seconds=seconds,
                                                         microseconds=microseconds)
