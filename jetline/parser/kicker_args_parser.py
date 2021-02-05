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

        # working directory
        parser.add_argument(
            '-w', '--working-dir', dest='working_dir', default=None,
            help='Absolute path or Relative path from Python execution environment'
        )

        # tries
        parser.add_argument(
            '-t', '--tries', dest='tries', type=int, default=1,
            help='the maximum number of attempts. default: 1.'
        )

        # delay
        parser.add_argument(
            '-l', '--delay', dest='delay', type=int, default=1,
            help='initial delay between attempts. default: 1.'
        )

        # backoff
        parser.add_argument(
            '-b', '--backoff', dest='backoff', type=int, default=1,
            help='multiplier applied to delay between attempts. default: 1 (no backoff).'
        )

        # jitter
        parser.add_argument(
            '-j', '--jitter', dest='jitter', type=KickerArgsParser._type_parse, default=0,
            help='extra seconds added to delay between attempts. default: 0.' \
                 'fixed if a number, random if a range tuple (min, max)'
        )

        # max_delay
        parser.add_argument(
            '-m', '--max-delay', dest='max_delay', type=int, default=None,
            help='the maximum value of delay. default: None (no limit).'
        )

        parsed_args = parser.parse_args(args)
        self._exec_yaml_path = parsed_args.yaml_file
        self._exec_date = parsed_args.exec_date
        self._working_dir = parsed_args.working_dir
        self._dry_run = parsed_args.dry_run
        self._tries = parsed_args.tries
        self._delay = parsed_args.delay
        self._backoff = parsed_args.backoff
        self._jitter = parsed_args.jitter
        self._max_delay = parsed_args.max_delay

    def exec_yaml_path(self):
        return self._exec_yaml_path

    def exec_date(self):
        return self._exec_date

    def working_dir(self):
        return self._working_dir

    def dry_run(self):
        return self._dry_run

    def tries(self):
        return self._tries

    def delay(self):
        return self._delay

    def backoff(self):
        return self._backoff

    def jitter(self):
        return self._jitter

    def max_delay(self):
        return self._max_delay

    @staticmethod
    def _type_parse(str_arg):
        try:
            any_obj = eval(str_arg)
        except:
            raise argparse.ArgumentTypeError('Invalid type', str_arg)
        return any_obj
