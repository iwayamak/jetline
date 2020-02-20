# -*- coding: utf-8 -*-

import os
import glob
import logging
from datetime import datetime
from ...module.module import Module
from ...share_parameter.share_parameter import ShareParameter
from ..abc.base_test_case import BaseTestCase

logger = logging.getLogger('jetline')


class TestModule(BaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestModule, self).__init__(*args, **kwargs)

    def test_parse_kick_args(self):
        yaml_name = 'test_postgresql_processing.yaml'
        date = '20200401'
        args = ['-y', yaml_name, '-d', date, '-w', 'test_dir']
        exec_yaml_name, dt_list, working_dir = Module.parse_kick_args(args)
        self.assertEqual(exec_yaml_name, yaml_name)
        self.assertEqual(dt_list, '20200401')
        self.assertEqual(working_dir, 'test_dir')

    def test_return_code(self):
        # success: 0
        exit_code = self._test_sub_module_run('test_postgresql_processing.yaml', True)
        self.assertEqual(0, exit_code)

        # error: 1
        exit_code = self._test_sub_module_run('test_postgresql_processing_error.yaml', True)
        self.assertEqual(1, exit_code)

        # success: 2
        ShareParameter.success_return_code = 2
        exit_code = self._test_sub_module_run('test_postgresql_processing.yaml', True)
        self.assertEqual(2, exit_code)
        ShareParameter.success_return_code = 0

        # error: 3x
        ShareParameter.error_return_code = 3
        exit_code = self._test_sub_module_run('test_postgresql_processing_error.yaml', True)
        self.assertEqual(3, exit_code)
        ShareParameter.error_return_code = 1

    @staticmethod
    def _test_sub_module_run(yaml_file_name: str, dry_run: bool = False):
        os.chdir(os.path.dirname(__file__))
        yaml_file_path = \
            os.path.join(
                os.path.join(os.path.dirname(__file__), 'sample_yaml'),
                yaml_file_name
            )
        date = datetime.now().strftime('%Y%m%d')
        args = ['-y', yaml_file_path, '-d', date]
        if dry_run:
            args.extend(['-D'])
        try:
            exec_yaml, exec_date, working_dir = Module.parse_kick_args(args)
            logger.info('module kicked...')
            logger.info('exec yaml: ' + exec_yaml)
            logger.info('exec_date: ' + exec_date)
            module = Module(exec_yaml, exec_date)
            module.set_up()
            module.execute()
            exit_code = ShareParameter.success_return_code
        except Exception as e:
            logger.exception(e)
            exit_code = ShareParameter.error_return_code
        return exit_code

    def tearDown(self):
        # remove result.yaml
        for f in glob.glob(os.path.join(os.path.dirname(__file__), 'test_*_result.yaml')):
            if os.path.isfile(f):
                os.remove(f)
        super().tearDown()

    def test_postgresql_processing_run(self):
        exit_code = self._test_sub_module_run('test_postgresql_processing.yaml')
        self.assertEqual(0, exit_code)

    def test_postgresql_processing_count_run(self):
        exit_code = self._test_sub_module_run('test_postgresql_processing_count.yaml')
        self.assertEqual(0, exit_code)

    def test_postgresql_copy_from_run(self):
        exit_code = self._test_sub_module_run('test_postgresql_copy_from.yaml')
        self.assertEqual(0, exit_code)

    def test_postgresql_copy_to_run(self):
        exit_code = self._test_sub_module_run('test_postgresql_copy_to.yaml')
        self.assertEqual(0, exit_code)

    def test_postgresql_copy_from_to_run(self):
        exit_code = self._test_sub_module_run('test_postgresql_copy_from_to.yaml')
        self.assertEqual(0, exit_code)

    def test_local_processing_copy_run(self):
        exit_code = self._test_sub_module_run('test_local_processing_copy.yaml')
        self.assertEqual(0, exit_code)

    def test_local_processing_remove_run(self):
        exit_code = self._test_sub_module_run('test_local_processing_remove.yaml')
        self.assertEqual(0, exit_code)

    def test_plugin_run(self):
        exit_code = self._test_sub_module_run('test_plugin.yaml')
        self.assertEqual(0, exit_code)
        exit_code = self._test_sub_module_run('column_join.yaml')
        self.assertEqual(0, exit_code)
        exit_code = self._test_sub_module_run('shell.yaml')
        self.assertEqual(0, exit_code)
        exit_code = self._test_sub_module_run('export_per_record.yaml')
        self.assertEqual(0, exit_code)
