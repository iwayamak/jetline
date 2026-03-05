"""日時操作ユーティリティ。."""

import time
from datetime import datetime

from dateutil import relativedelta


class TimeUtil:
    """日付文字列変換と日時演算を提供する。."""

    @classmethod
    def current_yyyymmddhhmiss(cls) -> str:
        """現在日時を `YYYYMMDDHHMISS` で返す。."""
        return datetime.now().strftime("%Y%m%d%H%M%S")

    @classmethod
    def current_yyyymmdd(cls) -> str:
        """現在日付を `YYYYMMDD` で返す。."""
        return datetime.now().strftime("%Y%m%d")

    @classmethod
    def datetime_object_from_yyyymmdd_str(cls, tstr: str) -> datetime:
        """`YYYYMMDD` 文字列を datetime へ変換する。."""
        return datetime.strptime(tstr, "%Y%m%d")

    @classmethod
    def yyyymmdd_str(cls, dt: datetime) -> str:
        """Datetime を `YYYYMMDD` 文字列へ変換する。."""
        return dt.strftime("%Y%m%d")

    @classmethod
    def datetime_list(cls, fr_str_yyyymmdd: str, to_str_yyyymmdd: str | None) -> list[datetime]:
        """開始日から終了日までの日付配列を返す。."""
        if to_str_yyyymmdd is None:
            return [cls.datetime_object_from_yyyymmdd_str(fr_str_yyyymmdd)]

        date_list: list[datetime] = []
        target_date_str = fr_str_yyyymmdd
        while True:
            target_date = cls.datetime_object_from_yyyymmdd_str(target_date_str)
            date_list.append(target_date)
            if target_date_str == to_str_yyyymmdd:
                break
            target_date_str = cls.yyyymmdd_str(
                target_date + relativedelta.relativedelta(days=1)
            )
        return date_list

    @classmethod
    def get_unix_time(cls, target_date: datetime) -> int:
        """Datetime の UNIX 時刻を返す。."""
        return int(time.mktime(target_date.timetuple()))

    @classmethod
    def datetime_delta(
        cls,
        target_date: datetime,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        leapdays: int = 0,
        weeks: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        microseconds: int = 0,
    ) -> datetime:
        """指定オフセットを加算した datetime を返す。."""
        return target_date + relativedelta.relativedelta(
            years=years,
            months=months,
            days=days,
            leapdays=leapdays,
            weeks=weeks,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds,
        )
