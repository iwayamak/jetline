# Plugin モジュール定義

`Plugin` は任意 Python クラスを読み込み、`run()` 相当の処理を実行します。

## `Plugin`（mode: `null`）

### 必須パラメータ

- `plugin_path` (str)
- `package` (str)
- `class_name` (str)

### 任意パラメータ

- `kwargs` (dict, default: `null`)

### 例

```yaml
sub_module:
  - name: Plugin
    mode: null
    param:
      plugin_path: plugin_module
      package: sample_command
      class_name: SampleCommand
      kwargs:
        key1: value1
```

## 注意

- `plugin_path` は実行時に参照可能なパスを指定してください。
- `kwargs` は対象クラスのコンストラクタ仕様に合わせて定義してください。
