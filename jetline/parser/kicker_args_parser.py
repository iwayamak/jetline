# -*- coding: utf-8 -*-

import argparse


class KickerArgsParser(object):

    EXEC_YAML = 'exec_yaml'
    FROM_EXEC_YYYYMMDD = 'from_exec_yyyymmdd'
    TO_EXEC_YYYYMMDD = 'to_exec_yyyymmdd'

    def __init__(self, args):
        parser = argparse.ArgumentParser('module starter')
        # yaml
        parser.add_argument('-y', '--yaml', dest='exec_yaml', required=True, help='yaml file path.')
        # exec date
        parser.add_argument('-d', '--exec-date', dest='exec_date', required=True, help='yyyymmdd. ex. 20140401')
        # dry run option
        parser.add_argument('-D', '--dry-run', action="store_true", default=False)
        parsed_args = parser.parse_args(args)
        self._exec_yaml = parsed_args.exec_yaml
        self._exec_date = parsed_args.exec_date
        self._dry_run = parsed_args.dry_run

    def exec_yaml(self):
        return self._exec_yaml

    def exec_date(self):
        return self._exec_date

    def dry_run(self):
        return self._dry_run
