"""kicker_args_parser のテスト。."""

from freezegun import freeze_time

from jetline.parser.kicker_args_parser import KickerArgsParser

from ..abc.base_test_case import BaseTestCase


class TestKickerArgsParser(BaseTestCase):
    """引数パースとバリデーションの検証を行う。."""

    def __init__(self, *args, **kwargs):
        """テストケースを初期化する。.

        Args:
            *args: 親クラスへ渡す位置引数。
            **kwargs: 親クラスへ渡すキーワード引数。
        """
        super().__init__(*args, **kwargs)

    def test_shortened_option_name_full_argument(self):
        """短縮オプションで主要引数を指定できることを確認する。."""
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['-y', yaml_name, '-d', date, '-D']
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertTrue(k.dry_run())

    def test_full_option_name_full_argument(self):
        """ロングオプションで主要引数を指定できることを確認する。."""
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['--yaml', yaml_name, '--exec-date', date, '--dry-run']
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertTrue(k.dry_run())

    def test_shortened_option_name_dry_run_false(self):
        """`-D` 未指定時に dry_run が偽になることを確認する。."""
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['-y', yaml_name, '-d', date]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())

    def test_full_option_name_dry_run_false(self):
        """`--dry-run` 未指定時に dry_run が偽になることを確認する。."""
        yaml_name = 'test.yaml'
        date = '20200401'
        args = ['--yaml', yaml_name, '--exec-date', date]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())

    @freeze_time('2112-09-03')
    def test_default_exec_date(self):
        """実行日未指定時に当日が設定されることを確認する。."""
        yaml_name = 'test.yaml'
        date = '21120903'
        args = ['--yaml', yaml_name]
        k = KickerArgsParser(args)
        self.assertEqual(k.exec_yaml_path(), yaml_name)
        self.assertEqual(k.exec_date(), date)
        self.assertFalse(k.dry_run())

    def test_jitter_tuple_parse(self):
        """Jitter タプル文字列が正しく解釈されることを確認する。."""
        args = ['--yaml', 'test.yaml', '--jitter', '(1, 3)']
        k = KickerArgsParser(args)
        self.assertEqual(k.jitter(), (1, 3))

    def test_invalid_exec_date(self):
        """不正な実行日形式でエラーになることを確認する。."""
        args = ['--yaml', 'test.yaml', '--exec-date', '2026-03-05']
        with self.assertRaises(SystemExit):
            KickerArgsParser(args)

    def test_invalid_retry_options(self):
        """不正なリトライ引数でエラーになることを確認する。."""
        with self.assertRaises(SystemExit):
            KickerArgsParser(['--yaml', 'test.yaml', '--tries', '0'])
        with self.assertRaises(SystemExit):
            KickerArgsParser(['--yaml', 'test.yaml', '--delay', '-1'])
        with self.assertRaises(SystemExit):
            KickerArgsParser(['--yaml', 'test.yaml', '--backoff', '0'])
        with self.assertRaises(SystemExit):
            KickerArgsParser(['--yaml', 'test.yaml', '--max-delay', '-1'])
