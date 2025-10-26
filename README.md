# PyReplacer

`config.yaml` ファイルで定義された一連のルールに基づいて、テキストファイル内の文字列を置換するためのPythonスクリプト群です。

## プログラムの構成

*   `runner.py`: メインの実行スクリプト。`config.yaml` を読み込み、定義されたジョブとワークフローを実行します。
*   `text_replacer_*.py`: それぞれが特定の置換機能を提供するモジュールです。
    *   `text_replacer.py`: 単純な文字列置換
    *   `text_replacer_from_list.py`: リストの要素で順番に置換
    *   `text_multi_replacer_from_lists.py`: 複数のルールリストに基づいて置換
    *   `text_replacer_with_complex_pattern.py`: 可変長のワイルドカードを含む複雑なパターンで置換
    *   `text_replacer_with_count_based_list.py`: 文字列の出現回数に基づいて置換
    *   `text_replacer_with_left_context.py`: キーワードの左側の文脈を含めて置換
    *   `text_replacer_with_right_context.py`: キーワードの右側の文脈を含めて置換
    *   `text_replacer_with_sequence.py`: 連番で置換

## `config.yaml` の主要セクション

`config.yaml` は、置換処理の動作を定義するための中核となるファイルです。

### `io`

入出力ファイルパスを指定します。

*   `input_path`: 読み込むファイルのパス。
*   `output_path`: 結果を書き出すファイルのパス。ジョブ実行時に `{job_name}` のようなプレースホルダーを使用できます。

```yaml
io:
  input_path: "input.txt"
  output_path: "output_{job_name}.txt"
```

### `params`

各置換モジュールに渡すパラメータのセットを定義します。ここで定義した名前を `workflow` や `jobs` から参照します。

```yaml
params:
  replace_apple:
    find_str: "APPLE"
    replacement_list: ["りんご", "アッポー"]
  replace_orange:
    find_str: "ORANGE"
    replacement_list: ["みかん"]
```

### `workflow`

実行する置換処理のシーケンス（ワークフロー）をリストで定義します。各ステップでは、使用するモジュールと、`params` で定義したパラメータセットへの参照 (`params_ref`) を指定します。

```yaml
workflow:
  - module: "text_replacer_from_list"
    params_ref: "replace_apple"
  - module: "text_replacer_from_list"
    params_ref: "replace_orange"
```

### `jobs`

複数の異なる置換タスク（ジョブ）をまとめて定義する場合に使用します。各ジョブは、ベースとなる `params` や `workflow` を上書き（オーバーライド）することができます。`jobs` を定義すると、`runner.py` は各ジョブを順番に実行します。

```yaml
jobs:
  job1:
    overrides:
      params:
        replace_apple:
          replacement_list: ["林檎"] # job1ではこのリストを使用
  job2:
    overrides:
      workflow: # job2ではこのワークフローを適用
        - module: "text_replacer"
          params_ref: "some_other_params"
```

## 実行方法

1.  `config.yaml` をプロジェクトのルートに配置します。
2.  入力ファイルを準備します。
3.  以下のコマンドを実行します。

    ```bash
    python PyReplacer/runner.py
    ```
