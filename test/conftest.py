
"""pytest 全体設定。統合テストの既定スキップを提供する。."""

import os
from pathlib import Path

import pytest

INTEGRATION_PATH_KEYWORDS = (
    'test/command/api/',
    'test/command/db/',
    'test/command/s3/',
    'test/command/scp/',
    'test/command/test_command_queue.py',
    'test/module/test_module.py',
)


def pytest_addoption(parser):
    """Pytest オプションを追加する。.

    Args:
        parser: pytest のオプションパーサ。
    """
    parser.addoption(
        '--run-integration',
        action='store_true',
        default=False,
        help='外部サービスが必要な統合テストを実行する',
    )


def pytest_configure(config):
    """Pytest 初期設定を行う。.

    Args:
        config: pytest 設定オブジェクト。
    """
    config.addinivalue_line('markers', 'integration: 統合テスト')
    # 実行ディレクトリに依存しないよう設定パスを固定する。
    settings_root = Path(__file__).resolve().parents[1] / 'jetline' / 'settings'
    os.environ.setdefault('JETLINE_SETTINGS', str(settings_root))


def pytest_collection_modifyitems(config, items):
    """収集済みテストに統合テストマーカーと skip 条件を適用する。.

    Args:
        config: pytest 設定オブジェクト。
        items: 収集済みテストアイテム。
    """
    run_integration = config.getoption('--run-integration')
    skip_marker = pytest.mark.skip(reason='統合テスト（--run-integration で実行）')
    for item in items:
        node_id = item.nodeid.replace('\\', '/')
        if any(keyword in node_id for keyword in INTEGRATION_PATH_KEYWORDS):
            item.add_marker('integration')
            if not run_integration:
                item.add_marker(skip_marker)
