# jetline

YAML 定義でバッチ処理を実行する ETL フレームワークです。  
古い設計を整理し、現在は「ローカルで回しやすい」「失敗時に追いやすい」「テストしやすい」構成に改善しています。

## 特徴

- YAML ベースで処理フロー（sub_module）を定義
- `jetline` コマンドで実行可能
- リトライ設定（tries/delay/backoff/jitter/max-delay）対応
- dry-run 対応
- pytest によるテスト実行（統合テストは明示実行）

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
pip install -e . --no-build-isolation
```

## 実行方法

```bash
jetline --yaml /path/to/job.yaml --exec-date 20260305
```

または

```bash
python -m jetline.cli --yaml /path/to/job.yaml
```

## YAML 定義書

モジュールごとの YAML 定義は `docs/` に分離しています。

- 全体ガイド: [docs/yaml/overview.md](docs/yaml/overview.md)
- PostgreSQL: [docs/yaml/postgresql.md](docs/yaml/postgresql.md)
- S3: [docs/yaml/s3.md](docs/yaml/s3.md)
- SCP: [docs/yaml/scp.md](docs/yaml/scp.md)
- LocalProcessing: [docs/yaml/local_processing.md](docs/yaml/local_processing.md)
- Plugin: [docs/yaml/plugin.md](docs/yaml/plugin.md)
- 結果YAMLメタデータ: [docs/yaml/result_metadata.md](docs/yaml/result_metadata.md)
- 日付プレースホルダ: [docs/yaml/overview.md#7-日付プレースホルダ](docs/yaml/overview.md#7-%E6%97%A5%E4%BB%98%E3%83%97%E3%83%AC%E3%83%BC%E3%82%B9%E3%83%9B%E3%83%AB%E3%83%80)

最小サンプル:

```yaml
sub_module:
  - name: LocalProcessing
    mode: Copy
    param:
      source_path: data/input.csv
      destination_path: tmp/input.csv
```

## CLI オプション

```text
-y, --yaml         実行する YAML ファイル（必須）
-d, --exec-date    実行日 (YYYYMMDD)
-D, --dry-run      dry-run モード
-w, --working-dir  作業ディレクトリ
-t, --tries        リトライ回数（1以上）
-l, --delay        初回待機秒（0以上）
-b, --backoff      バックオフ倍率（1以上）
-j, --jitter       ジッター（数値 or タプル/リスト。例: "(1, 3)"）
-m, --max-delay    最大待機秒（0以上）
```

## テスト

```bash
# ローカル単体テスト（デフォルト）
pytest -q

# 外部サービスが必要な統合テストも含める
pytest -q --run-integration
```

`--run-integration` を付けない場合、DB/S3/SCP を利用するテストは自動で skip されます。

## 結果YAML（メタデータ）

実行後に `*_result.yaml` が出力され、`metadata` に実行統計が保存されます。

```yaml
metadata:
  sub_module_creator_metrics:
    lazy_hit: 2
    lazy_miss: 1
    full_scan_parameter: 0
    full_scan_sub_module: 0
  command_metrics:
    total: 5
    succeeded: 4
    failed: 1
    by_name:
      CopyCommand:
        executed: 2
        succeeded: 2
        failed: 0
        elapsed_seconds_total: 0.0123
    by_sub_module:
      LocalProcessingCopy:
        total: 2
        succeeded: 2
        failed: 0
        by_name:
          CopyCommand:
            executed: 2
            succeeded: 2
            failed: 0
            elapsed_seconds_total: 0.0123
    failures:
      - command_name: RemoveCommand
        sub_module_name: LocalProcessingRemove
        error_type: FileNotFoundError
        error_message: "..."
        failed_at: "2026-03-05T14:10:00"
        tries_count: 1
  sub_module_summary:
    LocalProcessingCopy:
      total: 2
      succeeded: 2
      failed: 0
      success_rate: 100.0
      elapsed_seconds_total: 0.0123
      failed_commands: []
  execution_context:
    exec_yaml_path: /path/to/job.yaml
    exec_date: "20260305"
    dry_run_mode: false
    tries_count: 1
```

## 品質チェック

```bash
# Docstring (Googleスタイル) を含む静的解析
ruff check \
  jetline/cli.py \
  jetline/container/container.py \
  jetline/command/abc/command.py \
  jetline/command/abc/subprocess_command.py \
  jetline/command/command_queue.py \
  jetline/module/module.py \
  jetline/module/sub_module/abc/sub_module.py \
  jetline/module/sub_module/sub_module_creator.py \
  jetline/parser/kicker_args_parser.py \
  jetline/runtime/execution_context.py \
  jetline/share_parameter/share_parameter.py

# 型チェック（段階導入の中核ファイル）
mypy
```

## 直近の抜本改善

- 実行エントリを `jetline` / `jetline.cli` に統一
- 引数解析を dataclass 化し、実行設定を明示モデル化
- `eval` 廃止（安全な jitter 解析へ変更）
- `--exec-date` の厳密バリデーション追加
- リトライ設定の扱いを整理（責務分離）
- `Container` の初期化・クラス探索を再設計（再初期化バグ修正＋キャッシュ）
- ログ出力先ディレクトリを自動生成
- Python 3.13 互換の依存関係に更新

## 注意

- 既存の `kicker.py` は互換用ラッパーとして残しています。
- 実運用の統合テストは、接続先（DB/S3/SCP）を適切に設定して実行してください。
