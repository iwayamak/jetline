"""TimeUtil のユニットテスト。."""

import datetime

from freezegun import freeze_time

from jetline.util.time_util import TimeUtil
from test.abc.base_test_case import BaseTestCase


@freeze_time("2020-04-01 12:34:56")
class TestTimeUtil(BaseTestCase):
    """TimeUtil の日時処理を検証する。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。."""
        super().__init__(*args, **kwargs)

    def test_current_yyyymmddhhmiss(self):
        """現在日時文字列（秒付き）が返ることを確認する。."""
        current_datetime = TimeUtil.current_yyyymmddhhmiss()
        self.assertEqual(current_datetime, "20200401123456")

    def test_current_yyyymmdd(self):
        """現在日付文字列が返ることを確認する。."""
        current_datetime = TimeUtil.current_yyyymmdd()
        self.assertEqual(current_datetime, "20200401")

    def test_datetime_object_from_yyyymmdd_str(self):
        """日付文字列が datetime へ変換できることを確認する。."""
        dt = TimeUtil.datetime_object_from_yyyymmdd_str("20200401")
        self.assertEqual(dt.year, 2020)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 1)

    def test_yyyymmdd_str(self):
        """Datetime を日付文字列へ変換できることを確認する。."""
        dt_str = TimeUtil.yyyymmdd_str(datetime.datetime.strptime("20200401", "%Y%m%d"))
        self.assertEqual(dt_str, "20200401")

    def test_datetime_list_multiple(self):
        """開始日から終了日までの日付配列を生成できることを確認する。."""
        date_list = TimeUtil.datetime_list("20200401", "20200403")
        self.assertEqual(len(date_list), 3)
        self.assertEqual((date_list[0].year, date_list[0].month, date_list[0].day), (2020, 4, 1))
        self.assertEqual((date_list[1].year, date_list[1].month, date_list[1].day), (2020, 4, 2))
        self.assertEqual((date_list[2].year, date_list[2].month, date_list[2].day), (2020, 4, 3))

    def test_datetime_list_single(self):
        """終了日未指定時に1件配列となることを確認する。."""
        date_list = TimeUtil.datetime_list("20200401", None)
        self.assertEqual(len(date_list), 1)
        self.assertEqual((date_list[0].year, date_list[0].month, date_list[0].day), (2020, 4, 1))

    def test_get_unix_time(self):
        """Datetime から UNIX 時刻へ変換できることを確認する。."""
        target_date = datetime.datetime.strptime("2015/02/15 10:11:12", "%Y/%m/%d %H:%M:%S")
        unix_time = TimeUtil.get_unix_time(target_date)
        self.assertEqual(unix_time, 1423962672)

    def test_datetime_delta(self):
        """オフセット加算が正しく行えることを確認する。."""
        target_date = datetime.datetime.strptime("2015/02/15 10:11:12", "%Y/%m/%d %H:%M:%S")
        after_date = datetime.datetime.strptime("2016/04/18 14:16:18", "%Y/%m/%d %H:%M:%S")
        delta_date = TimeUtil.datetime_delta(
            target_date,
            years=1,
            months=2,
            days=3,
            hours=4,
            minutes=5,
            seconds=6,
        )
        self.assertEqual(delta_date, after_date)
