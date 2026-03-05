# YAML 定義ガイド（全体）

## 1. ルート構造

```yaml
sub_module:
  - name: <モジュール名>
    mode: <モード名または null>
    param:
      <キー>: <値>
```

- `sub_module` は必須で、配列である必要があります。
- 各要素は必ず `name` / `mode` / `param` を持つ必要があります。
- `param` は辞書である必要があります。

## 2. 利用可能なモジュール名

- `PostgreSQLProcessing`
- `PostgreSQLCopy`
- `LocalProcessing`
- `S3`
- `Scp`
- `Plugin`

## 3. mode の指定ルール

- `name: PostgreSQLCopy` は `mode: From` または `mode: To`
- `name: PostgreSQLProcessing` は `mode: Count` または `mode: null`（通常実行）
- `name: LocalProcessing` は `mode: Copy` または `mode: Remove`
- `name: S3` は `mode: Put` / `Get` / `List`
- `name: Scp` は `mode: Put` / `Get`
- `name: Plugin` は `mode: null`

## 4. 最小サンプル

```yaml
sub_module:
  - name: PostgreSQLProcessing
    mode: null
    param:
      postgresql_component_key: POSTGRESQL_COMPONENT.ID=UT
      sql_file_name: sql/query.sql
```

## 5. 注意点

- 未定義キーは実行に使われません（typo の温床になるため注意）。
- `component_key` 系は `xxx_COMPONENT.ID=yyy` 形式で指定します。
- パス指定は実行時カレントディレクトリ基準です。

## 6. 結果YAML

- 実行後に `*_result.yaml` が出力されます。
- `metadata` に `sub_module_creator_metrics` / `command_metrics` / `sub_module_summary` / `execution_context` が記録されます。
- `command_metrics.failures` には `failed_at` と `tries_count` も含まれるため、障害調査時に再試行回数と発生時刻を追跡できます。

## 7. 日付プレースホルダ

`--exec-date` は `YYYYMMDD` 固定ですが、SQL や各種テンプレート内では `exec_date(...)` で相対日付を扱えます。

### 主要関数

- `exec_date(format_str="%Y%m%d", years=None, months=None, days=None)`
- `timestamp(format_str="%Y%m%d", years=None, months=None, days=None)`（現在時刻基準）

### 例

```jinja2
{{ exec_date(days=-1) }}       # 昨日
{{ exec_date(days=-7) }}       # 1週間前
{{ exec_date(months=-1) }}     # 1ヶ月前
{{ exec_date(years=-1) }}      # 1年前
{{ exec_date("%Y-%m-%d", days=-1) }}
```

### 注意

- `DAY-1` のような文字列はサポートしていません。
- 相対日付はプレースホルダ関数で指定してください。
