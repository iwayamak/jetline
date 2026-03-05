# SCP モジュール定義

## 1. `Scp`（mode: `Put`）

ローカルからリモートへ転送します。

### 必須パラメータ

- `scp_component_key` (str)
- `local_path` (str)
- `remote_dir_path` (str)

### 任意パラメータ

- `recursive` (bool, default: `false`)
- `preserve_times` (bool, default: `false`)
- `use_last_result` (bool, default: `false`)

### 例

```yaml
sub_module:
  - name: Scp
    mode: Put
    param:
      scp_component_key: SCP_COMPONENT.ID=UT
      local_path: data/*.csv
      remote_dir_path: /var/tmp/inbox
      recursive: false
      preserve_times: true
```

## 2. `Scp`（mode: `Get`）

リモートからローカルへ取得します。

### 必須パラメータ

- `scp_component_key` (str)
- `remote_path` (str)
- `local_dir_path` (str)

### 任意パラメータ

- `recursive` (bool, default: `false`)
- `preserve_times` (bool, default: `false`)

### 例

```yaml
sub_module:
  - name: Scp
    mode: Get
    param:
      scp_component_key: SCP_COMPONENT.ID=UT
      remote_path: /var/tmp/inbox/*.csv
      local_dir_path: tmp/get
      preserve_times: true
```

## 注意

旧サンプルで見かける `preserve_time` / `preserve` は現行実装の正式キーではありません。`preserve_times` を使用してください。
