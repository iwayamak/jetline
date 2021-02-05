# -*- coding: utf-8 -*-

import datetime
from freezegun import freeze_time
from ..abc.base_test_case import BaseTestCase
from jetline.util.time_util import TimeUtil


@freeze_time('2020-04-01 12:34:56')
class TestTimeUtil(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_current_yyyymmddhhmiss(self):
        current_datetime = TimeUtil.current_yyyymmddhhmiss()
        self.assertEqual(current_datetime, '20200401123456')

    def test_current_yyyymmdd(self):
        current_datetime = TimeUtil.current_yyyymmdd()
        self.assertEqual(current_datetime, '20200401')

    def test_datetime_object_from_yyyymmdd_str(self):
        dt = TimeUtil.datetime_object_from_yyyymmdd_str('20200401')
        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 1)

    def test_yyyymmdd_str(self):
        str = \
            TimeUtil.yyyymmdd_str(
                datetime.datetime.strptime('20200401', '%Y%m%d')
            )
        self.assertEqual(str, '20200401')

    def test_datetime_list_multiple(self):
        lst = TimeUtil.datetime_list('20200401', '20200403')
        self.assertEqual(len(lst), 3)
        d20200401 = lst[0]
        self.assertEqual(d20200401.year, 2020)
        self.assertEqual(d20200401.month, 4)
        self.assertEqual(d20200401.day, 1)
        d20200402 = lst[1]
        self.assertEqual(d20200402.year, 2020)
        self.assertEqual(d20200402.month, 4)
        self.assertEqual(d20200402.day, 2)
        d20200403 = lst[2]
        self.assertEqual(d20200403.year, 2020)
        self.assertEqual(d20200403.month, 4)
        self.assertEqual(d20200403.day, 3)

    def test_datetime_list_single(self):
        lst = TimeUtil.datetime_list('20200401', None)
        self.assertEqual(len(lst), 1)
        d20200401 = lst[0]
        self.assertEqual(d20200401.year, 2020)
        self.assertEqual(d20200401.month, 4)
        self.assertEqual(d20200401.day, 1)

    def test_get_unix_time(self):
        target_date = \
            datetime.datetime.strptime(
                '2015/02/15 10:11:12', '%Y/%m/%d %H:%M:%S'
            )
        unix_time = TimeUtil.get_unix_time(target_date)
        self.assertEqual(unix_time, 1423962672)

    def test_datetime_delta(self):
        target_date = \
            datetime.datetime.strptime(
                '2015/02/15 10:11:12', '%Y/%m/%d %H:%M:%S'
            )
        after_date = \
            datetime.datetime.strptime(
                '2016/04/18 14:16:18', '%Y/%m/%d %H:%M:%S'
            )
        delta_date = \
            TimeUtil.datetime_delta(
                target_date, years=1, months=2, days=3,
                hours=4, minutes=5, seconds=6
            )
        self.assertEqual(delta_date, after_date)
