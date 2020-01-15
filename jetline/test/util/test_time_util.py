# -*- coding: utf-8 -*-

import unittest
import datetime
from ...util.time_util import TimeUtil


class TestTimeUtil(unittest.TestCase):

    def test_current_yyyymmddhhmiss(self):
        current_datetime = TimeUtil.current_yyyymmddhhmiss()

    def test_current_yyyymmdd(self):
        current_datetime = TimeUtil.current_yyyymmdd()

    def test_datetime_object_from_yyyymmdd_str(self):
        dt = TimeUtil.datetime_object_from_yyyymmdd_str('20140401')
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 1)

    def test_yyyymmdd_str(self):
        str = \
            TimeUtil.yyyymmdd_str(
                datetime.datetime.strptime('20140401', '%Y%m%d')
            )
        self.assertEqual(str, '20140401')

    def test_datetime_list(self):
        lst = TimeUtil.datetime_list('20140401', '20140403')
        d20140401 = lst[0]
        self.assertEqual(d20140401.year, 2014)
        self.assertEqual(d20140401.month, 4)
        self.assertEqual(d20140401.day, 1)
        d20140402 = lst[1]
        self.assertEqual(d20140402.year, 2014)
        self.assertEqual(d20140402.month, 4)
        self.assertEqual(d20140402.day, 2)
        d20140403 = lst[2]
        self.assertEqual(d20140403.year, 2014)
        self.assertEqual(d20140403.month, 4)
        self.assertEqual(d20140403.day, 3)

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
