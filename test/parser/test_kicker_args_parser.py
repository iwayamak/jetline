# -*- coding: utf-8 -*-

from freezegun import freeze_time
from jetline.parser.kicker_args_parser import KickerArgsParser
from ..abc.base_test_case import BaseTestCase


class TestKickerArgsParser(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestKickerArgsParser, self).__init__(*args, **kwargs)

    def test_shortened_option_name_full_argument(self):
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['-y', yaml_name, '-d', date, '-D']
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertTrue(k.dry_run())

    def test_full_option_name_full_argument(self):
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['--yaml', yaml_name, '--exec-date', date, '--dry-run']
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertTrue(k.dry_run())

    def test_shortened_option_name_dry_run_false(self):
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['-y', yaml_name, '-d', date]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())

    def test_full_option_name_dry_run_false(self):
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['--yaml', yaml_name, '--exec-date', date]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())

    @freeze_time('2112-09-03')
    def test_default_exec_date(self):
        yaml_name = 'test.yaml'
        date = '21120903'
        args = ['--yaml', yaml_name]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())
