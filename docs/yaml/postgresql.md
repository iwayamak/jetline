# PostgreSQL モジュール定義

## 1. `PostgreSQLProcessing`（mode: `null`）

SQL を実行します。

### 必須パラメータ

- `postgresql_component_key` (str)
- `sql_file_name` (str)

### 任意パラメータ

- `input_value` (dict, default: `null`)

### 例

```yaml
sub_module:
  - name: PostgreSQLProcessing
    mode: null
    param:
      postgresql_component_key: POSTGRESQL_COMPONENT.ID=UT
      sql_file_name: sql/test_postgresql_processing.sql
      input_value:
        schema: public
        table: sample_table
```

## 2. `PostgreSQLProcessing`（mode: `Count`）

SQL 結果件数に対してアサーションします。

### 必須パラメータ

- `postgresql_component_key` (str)
- `sql_file_name` (str)

### 任意パラメータ

- `input_value` (dict, default: `null`)
- `assert_eq` (int, default: `null`)
- `assert_ne` (int, default: `null`)
- `assert_ge` (int, default: `null`)
- `assert_le` (int, default: `null`)

### 例

```yaml
sub_module:
  - name: PostgreSQLProcessing
    mode: Count
    param:
      postgresql_component_key: POSTGRESQL_COMPONENT.ID=UT
      sql_file_name: sql/test_postgresql_processing_count.sql
      assert_eq: 10
```

## 3. `PostgreSQLCopy`（mode: `To`）

SQL 結果を CSV に書き出します。

### 必須パラメータ

- `postgresql_component_key` (str)
- `sql_file_name` (str)
- `csv_file_name` (str)

### 任意パラメータ

- `delimiter` (str, default: `,`)
- `null_str` (str, default: `null`)
- `header` (bool, default: `true`)
- `quote` (str, default: `"`)
- `escape` (str, default: `"`)
- `force_quote_list` (list, default: `null`)
- `encoding` (str, default: `utf-8`)
- `gzip` (bool, default: `false`)
- `input_value` (dict, default: `null`)

### 例

```yaml
sub_module:
  - name: PostgreSQLCopy
    mode: To
    param:
      postgresql_component_key: POSTGRESQL_COMPONENT.ID=UT
      sql_file_name: sql/export.sql
      csv_file_name: out/result.csv
      header: true
      gzip: false
```

## 4. `PostgreSQLCopy`（mode: `From`）

CSV をテーブルへ取り込みます。

### 必須パラメータ

- `postgresql_component_key` (str)
- `table_name` (str)

### 条件付き必須

- `csv_file_name` (str)
  - `use_last_result: true` の場合は、直前サブモジュール結果を使うため未指定でも動作可能

### 任意パラメータ

- `column_list` (list, default: `null`)
- `delimiter` (str, default: `,`)
- `null_str` (str, default: `null`)
- `header` (bool, default: `true`)
- `quote` (str, default: `"`)
- `escape` (str, default: `"`)
- `encoding` (str, default: `utf8`)
- `gzip` (bool, default: `false`)
- `use_last_result` (bool, default: `false`)
- `remove_source_file` (bool, default: `false`)

### 例

```yaml
sub_module:
  - name: PostgreSQLCopy
    mode: From
    param:
      postgresql_component_key: POSTGRESQL_COMPONENT.ID=UT
      table_name: public.import_target
      csv_file_name: data/import.csv
      remove_source_file: false
```
