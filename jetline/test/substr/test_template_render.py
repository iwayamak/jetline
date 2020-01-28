# -*- coding: utf-8 -*-

import os
from freezegun import freeze_time
from ...substr.template_render import TemplateRender
from ...share_parameter.share_parameter import ShareParameter
from ...util.file_util import FileUtil
from ..abc.base_test_case import BaseTestCase


class TestTemplateRender(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self) -> None:
        ShareParameter.exec_date = '20200401'

    def test_batch_name(self):
        ShareParameter.batch_name = self.__class__.__name__
        correct_result = 'hello\'TestTemplateRender\' good-bye'
        template = TemplateRender(
            'hello\'{{batch_name}}\' good-bye'
        )
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_default_format(self):
        correct_result = 'hello\'20200401\' good-bye'
        template = TemplateRender(
            'hello\'{{exec_date()}}\' good-bye'
        )
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_set_format(self):
        correct_result = 'hello\'2020-04-01 00:00:00\' good-bye\'2020/04/01 00:00:00\''
        template = TemplateRender(
            'hello\'{{exec_date(\'%Y-%m-%d %H:%M:%S\')}}\' good-bye\'{{exec_date(\'%Y/%m/%d %H:%M:%S\')}}\''
        )
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_inc_days(self):
        correct_result = 'hello20200402 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', days=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_dec_days(self):
        correct_result = 'hello20200331 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', days=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_inc_months(self):
        correct_result = 'hello20200501 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', months=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_dec_months(self):
        correct_result = 'hello20200301 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', months=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_inc_years(self):
        correct_result = 'hello20210401 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', years=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_dec_years(self):
        correct_result = 'hello20190401 good-bye'
        template = TemplateRender('hello{{exec_date(\'%Y%m%d\', years=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_exec_date_sql_file(self):
        correct_result = 'select * from test_template_render_table where date_time = \'2020040100\';\n'
        result = \
            FileUtil.file_to_str(
                os.path.join(
                    os.path.dirname(__file__), 'test_template_render.sql'
                )
            )
        self.assertEqual(correct_result, result)

    def test_log_dir(self):
        ShareParameter.log_dir = '/tmp/logs'
        correct_result = 'hello\'/tmp/logs\' good-bye'
        template = TemplateRender(
            'hello\'{{log_dir}}\' good-bye'
        )
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_default_format(self):
        correct_result = 'hello\'20200401\' good-bye'
        template = TemplateRender('hello\'{{timestamp()}}\' good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_set_format(self):
        correct_result = 'hello\'2020-04-01 12:34:56\' good-bye\'2020/04/01 12:34:56\''
        template = TemplateRender('hello\'{{timestamp(\'%Y-%m-%d %H:%M:%S\')}}\' good-bye\'{{timestamp(\'%Y/%m/%d %H:%M:%S\')}}\'')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_inc_days(self):
        correct_result = 'hello20200402 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', days=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_dec_days(self):
        correct_result = 'hello20200331 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', days=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_inc_months(self):
        correct_result = 'hello20200501 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', months=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_dec_months(self):
        correct_result = 'hello20200301 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', months=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_inc_years(self):
        correct_result = 'hello20210401 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', years=+1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2020-04-01 12:34:56')
    def test_timestamp_dec_months(self):
        correct_result = 'hello20190401 good-bye'
        template = TemplateRender('hello{{timestamp(\'%Y%m%d\', years=-1)}} good-bye')
        result = template.apply()
        self.assertEqual(correct_result, result)
