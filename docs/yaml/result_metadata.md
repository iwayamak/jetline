# 結果YAMLメタデータ定義

## 1. 概要

実行後に出力される `*_result.yaml` には `metadata` が含まれます。  
この章では、`metadata` のキー定義を記載します。

## 2. 主要キー

- `sub_module_creator_metrics`: SubModule 解決時の統計
- `command_metrics`: Command 実行統計
- `sub_module_summary`: SubModule 単位の集計サマリー
- `execution_context`: 実行時コンテキスト

## 3. command_metrics の定義

```yaml
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
      error_message: "No such file or directory"
      failed_at: "2026-03-05T14:10:00"
      tries_count: 1
```

## 4. sub_module_summary の定義

`command_metrics.by_sub_module` から自動生成される要約です。

```yaml
sub_module_summary:
  LocalProcessingCopy:
    total: 2
    succeeded: 2
    failed: 0
    success_rate: 100.0
    elapsed_seconds_total: 0.0123
    failed_commands: []
  LocalProcessingRemove:
    total: 1
    succeeded: 0
    failed: 1
    success_rate: 0.0
    elapsed_seconds_total: 0.0045
    failed_commands:
      - RemoveCommand
```
