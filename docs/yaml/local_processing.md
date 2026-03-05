# LocalProcessing モジュール定義

## 1. `LocalProcessing`（mode: `Copy`）

ローカルパスをコピーします。

### 必須パラメータ

- `source_path` (str)
- `destination_path` (str)

### 例

```yaml
sub_module:
  - name: LocalProcessing
    mode: Copy
    param:
      source_path: data/input.csv
      destination_path: tmp/input.csv
```

## 2. `LocalProcessing`（mode: `Remove`）

ローカルファイル/ディレクトリを削除します。

### 必須パラメータ

- `path_list` (list[str])

### 任意パラメータ

- `use_last_result` (bool, default: `false`)

### 例

```yaml
sub_module:
  - name: LocalProcessing
    mode: Remove
    param:
      path_list:
        - tmp/*.csv
        - tmp/work
```
