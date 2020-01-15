# -*- coding: utf-8 -*-

import logging
from freezegun import freeze_time
from ...substr.template_yaml import TemplateYaml
from ...share_parameter.share_parameter import ShareParameter
from ...util.time_util import TimeUtil
from ..abc.base_test_case import BaseTestCase

logger = logging.getLogger('jetline')


class TestTemplateYaml(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_exec_date(self):
        logger.log_name = 'test'
        ShareParameter.exec_date = \
            TimeUtil.datetime_object_from_yyyymmdd_str('20140401')
        correct_result = '/tmp/20140401/file.txt'
        template = TemplateYaml('/tmp/${exec_date:%Y%m%d}/file.txt')
        result = template.apply()
        self.assertEqual(correct_result, result)
        correct_result = '/tmp/20140401000000/file.txt'
        template = \
            TemplateYaml(
                '/tmp/${exec_date:%Y%m%d%H%M%S}/file.txt'
            )
        result = template.apply()
        self.assertEqual(correct_result, result)

    @freeze_time('2016-03-16 12:34:56')
    def test_timestamp(self):
        logger.log_name = 'test'
        correct_result = '/tmp/20160316/file.txt'
        template = TemplateYaml('/tmp/${timestamp:%Y%m%d}/file.txt')
        result = template.apply()
        self.assertEqual(correct_result, result)
        correct_result = '/tmp/20160316123456/file.txt'
        template = TemplateYaml('/tmp/${timestamp:%Y%m%d%H%M%S}/file.txt')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_log_dir(self):
        logger.log_name = 'test'
        ShareParameter.log_dir = '/tmp/log'
        correct_result = '/tmp/log/file.txt'
        template = TemplateYaml('${log_dir}/file.txt')
        result = template.apply()
        self.assertEqual(correct_result, result)

    def test_batch_name(self):
        logger.log_name = 'test'
        ShareParameter.batch_name = 'TestTemplateYaml'
        correct_result = '/tmp/TestTemplateYaml/file.txt'
        template = TemplateYaml('/tmp/${batch_name}/file.txt')
        result = template.apply()
        self.assertEqual(correct_result, result)
