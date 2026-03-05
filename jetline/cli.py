
"""jetline の CLI エントリポイント。."""

import logging
import logging.config
import os
import sys

from jetline.module.module import Module
from jetline.parser.kicker_args_parser import KickerArgsParser
from jetline.share_parameter.share_parameter import ShareParameter
from jetline.util.path_util import PathUtil
from jetline.util.yaml_util import YamlUtil


def _init_logging() -> logging.Logger:
    """ロギング設定を初期化する。.

    Returns:
        logging.Logger: jetline ロガー。
    """
    PathUtil.mkdir_if_not_exists(PathUtil.logs_path())
    logging.config.dictConfig(YamlUtil.load_file(PathUtil.logging_conf_path()))
    return logging.getLogger('jetline')


def run(argv: list[str] | None = None) -> int:
    """CLI 実行本体。.

    Args:
        argv: 引数配列。省略時は `sys.argv[1:]` を使用。

    Returns:
        int: プロセス終了コード。
    """
    ShareParameter.reset()
    if argv is None:
        argv = sys.argv[1:]

    exit_code = ShareParameter.error_return_code
    module = None
    logger = None
    try:
        options = KickerArgsParser(argv).options()
        ShareParameter.dry_run_mode = options.dry_run
        Module.configure_retry_options(options.retry)

        if options.working_dir:
            os.chdir(options.working_dir)

        ShareParameter.batch_name = os.path.splitext(os.path.basename(options.yaml_file))[0]
        logger = _init_logging()
        logger.info('module kicked...')
        logger.info('exec yaml: %s', options.yaml_file)
        logger.info('exec_date: %s', options.exec_date)

        module = Module(options.yaml_file, options.exec_date)
        module.set_up()
        module.execute()
        exit_code = ShareParameter.success_return_code
    except Exception as exc:
        if logger is not None:
            logger.exception(exc)
        else:
            print(f'jetline failed before logger initialization: {exc}', file=sys.stderr)
        exit_code = ShareParameter.error_return_code
    finally:
        if module is not None:
            module.tear_down()
        if logger is not None:
            logger.info('module finished... exit_code: %s', str(exit_code))
    return exit_code


def main() -> None:
    """CLI エントリポイント。."""
    sys.exit(run())


if __name__ == '__main__':
    main()
