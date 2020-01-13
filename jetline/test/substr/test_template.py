# -*- coding: utf-8 -*-

import re
import logging
from freezegun import freeze_time
from ...substr.template import Template
from ...share_parameter.share_parameter import ShareParameter
from ...util.time_util import TimeUtil
from ..abc.base_test_case import BaseTestCase

logger = logging.getLogger('jetline')


class TestTemplate(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def is_match(input_str: str, output_str: str):
        template = Template('hoge')
        p = re.compile(template.PATTERN)
        ls = p.findall(input_str)
        print('matched str: ' + str(ls))
        if len(ls) == 0:
            return False
        for s in ls:
            if s != output_str:
                return False
        return True

    def test_val_pattern(self):
        self.assertFalse(self.is_match('aaa', 'aaa'))
        self.assertFalse(self.is_match('1', '1'))
        self.assertFalse(self.is_match('a1', 'a2'))
        self.assertFalse(self.is_match('1a', '1a'))
        self.assertTrue(self.is_match('${}', '${}'))
        self.assertFalse(self.is_match('$', '$'))
        self.assertFalse(self.is_match('${', '${'))
        self.assertFalse(self.is_match('${a', '${a'))
        self.assertFalse(self.is_match('${1', '${1'))
        self.assertFalse(self.is_match('${a1', '${a1'))
        self.assertFalse(self.is_match('}', '}'))
        self.assertFalse(self.is_match('a}', 'a}'))
        self.assertFalse(self.is_match('0}', '0}'))
        self.assertFalse(self.is_match('$}', '$}'))
        self.assertFalse(self.is_match('{', '{'))
        self.assertFalse(self.is_match('{}', '{}'))
        self.assertTrue(self.is_match('${aaa}', '${aaa}'))
        self.assertFalse(self.is_match('${aaa}', '${aab}'))
        self.assertTrue(self.is_match('${aa a}', '${aa a}'))
        self.assertTrue(self.is_match('${aaa001}', '${aaa001}'))
        self.assertTrue(self.is_match('${aaa_001}', '${aaa_001}'))
        self.assertTrue(self.is_match('hello ${aaa_001}goodbye', '${aaa_001}'))

    def test_val_method_pattern(self):
        self.assertTrue(self.is_match('${aa.aa}', '${aa.aa}'))
        self.assertTrue(self.is_match('${aa.aa()}', '${aa.aa()}'))

    def test_exec_date(self):
        logger.log_name = 'test'
        ShareParameter.exec_date = TimeUtil.datetime_object_from_yyyymmdd_str('20140401')
        correct_result = 'hello\'2014-04-01 00:00:00\' good-bye'
        template = Template('hello${exec_date} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        correct_result = 'hello\'2014-04-01 00:00:00\' good-bye\'2014/04/01 00:00:00\''
        template = Template('hello${exec_date} good-bye${exec_date:%Y/%m/%d %H:%M:%S}')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        correct_result = 'hello20140401 good-bye'
        template = Template('hello${exec_date:%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        correct_result = 'hello20140402 good-bye'
        template = Template('hello${exec_date(days=1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        ShareParameter.exec_date = TimeUtil.datetime_object_from_yyyymmdd_str('20120229')
        correct_result = 'hello20110228 good-bye'
        template = Template('hello${exec_date(years=-1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        correct_result = 'hello20130228 good-bye'
        template = Template('hello${exec_date(years=1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
        ShareParameter.exec_date = TimeUtil.datetime_object_from_yyyymmdd_str('20120331')
        correct_result = 'hello20120229 good-bye'
        template = Template('hello${exec_date(months=-1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

    @freeze_time('2016-03-16 12:34:56')
    def test_timestamp(self):
        logger.log_name = 'test'
        correct_result = 'hello\'2016-03-16 12:34:56\' good-bye'
        template = Template('hello${timestamp} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello\'2016-03-16 12:34:56\' good-bye\'2016/03/16 12:34:56\''
        template = Template('hello${timestamp} good-bye${timestamp:%Y/%m/%d %H:%M:%S}')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello20160316 good-bye'
        template = Template('hello${timestamp:%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello20160317 good-bye'
        template = Template('hello${timestamp(days=1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello20150316 good-bye'
        template = Template('hello${timestamp(years=-1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello20170316 good-bye'
        template = Template('hello${timestamp(years=1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)

        correct_result = 'hello20160216 good-bye'
        template = Template('hello${timestamp(months=-1):%Y%m%d} good-bye')
        result = template.apply()
        print(result)
        self.assertEqual(correct_result, result)
