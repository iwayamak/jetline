# -*- coding: utf-8 -*-

import datetime
import argparse


class KickerArgsParser(object):

    def __init__(self, args):
        parser = \
            argparse.ArgumentParser(
                prog='kicker.py',
            )
        # yaml
        parser.add_argument(
            '-y', '--yaml', dest='yaml_file', required=True,
            help='yaml file path.'
        )
        # exec date
        parser.add_argument(
            '-d', '--exec-date', dest='exec_date',
            default=datetime.datetime.now().strftime('%Y%m%d'),
            help='execution date in `yyyymmdd` format: e.g. 20200401'
        )
        # dry run option
        parser.add_argument(
            '-D', '--dry-run', action="store_true", default=False,
            help='perform a dry run'
        )
        parsed_args = parser.parse_args(args)
        self._exec_yaml_path = parsed_args.yaml_file
        self._exec_date = parsed_args.exec_date
        self._dry_run = parsed_args.dry_run

    def exec_yaml_path(self):
        return self._exec_yaml_path

    def exec_date(self):
        return self._exec_date

    def dry_run(self):
        return self._dry_run
