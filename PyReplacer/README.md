# PyReplacer

`config.yaml` ファイルで定義された一連のルールに基づいて、テキストファイル内の文字列を置換するためのPythonスクリプト群です。

## プログラムの構成

*   `src/runner.py`: メインの実行スクリプト。`config.yaml` を読み込み、定義されたジョブとワークフローを実行します。
*   `src/text_replacer_*.py`: それぞれが特定の置換機能を提供するモジュールです。
    *   `text_replacer_contextual.py`: 単純な文字列置換、および左右の文脈を含めた置換（統合版）
    *   `text_replacer_from_list.py`: リストの要素で順番に置換
    *   `text_multi_replacer_from_lists.py`: 複数のルールリストに基づいて置換
    *   `text_replacer_with_complex_pattern.py`: 可変長のワイルドカードを含む複雑なパターンで置換
    *   `text_replacer_with_count_based_list.py`: 文字列の出現回数に基づいて置換
    *   `text_replacer_with_sequence.py`: 連番で置換
*   `tests/`: 各モジュールの単体テスト。
*   `config.yaml`: 置換処理の動作を定義する設定ファイル。
*   `README.md`: このファイル。

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

各置換モジュールで使用するパラメータのセットを定義します。このセクションは、処理の「レシピ」集のようなものです。

```yaml
params:
  # --- 複数の単語を一度に置換 ---
  # from: text_multi_replacer_from_lists.py
  multi_word_replace_params:
    replacement_rules:
      - find_string: 'APPLE'
        replacement_list: ['りんご', '青りんご']
        loop: true  # loop:true の場合、リストを循環して使用します
      - find_string: 'ORANGE'
        replacement_list: ['みかん', 'オレンジ']
        # loop指定がない場合、リストの最後の要素を使い続けます

  # --- 連番に置換 ---
  # from: text_replacer_with_sequence.py
  sequence_replace_params:
    string_to_find: 'ITEM:'
    start_number: 1
    format_string: '項目{}:' # {} の部分が連番に置き換わります

  # --- 文脈に応じて置換（統合版） ---
  # from: text_replacer_contextual.py
  simple_contextual_params:
    string_to_find: "2025"
    string_to_replace_with: "2026"

  left_context_params:
    string_to_find: 'キーワード'
    string_to_replace_with: '【重要】'
    left_context_length: 3 # キーワードの左側、最大3文字を含めて置換します

  right_context_params:
    string_to_find: 'です'
    string_to_replace_with: 'でした。'
    right_context_length: 1 # 「です」の右側、最大1文字(。)を含めて置換します

  # --- 複雑なパターンで置換 (from: text_replacer_with_complex_pattern.py) ---
  complex_pattern_params:
    string_to_find_1: '開始'
    string_to_find_2: '終了'
    string_to_replace_with: '【パターンマッチ】'
    min_len: 3
    max_len: 5 # 3～5文字の範囲にマッチ

  # --- リストから順番に置換 ---
  # from: text_replacer_from_list.py
  sequential_list_params:
    string_to_find: 'LIST_REPLACE'
    replacement_list: ['A', 'B', 'C']
    loop: true # loop:true の場合、リストを循環して使用します

  # --- 回数ベースでリストから置換 ---
  # from: text_replacer_with_count_based_list.py
  count_based_list_params:
    string_to_find: 'COUNT_TARGET'
    replacement_rules:
      - ['FIRST', 2]  # 1-2回目
      - ['SECOND', 4] # 3-4回目
      - ['THIRD', 5]  # 5回目以降
```

### `workflow`

実行する置換処理のシーケンス（ワークフロー）をリストで定義します。各ステップでは、使用するモジュールと、`params` で定義したパラメータセットへの参照 (`param_set`) を指定します。

```yaml
workflow:
  - function: "replace_string_contextual"
    param_set: "simple_contextual_params"
  - function: "replace_string_contextual"
    param_set: "left_context_params"
```

### `jobs`

複数の異なる置換タスク（ジョブ）をまとめて定義する場合に使用します。各ジョブは、ベースとなる `params` や `workflow` を上書き（オーバーライド）することができます。`jobs` を定義すると、`runner.py` は各ジョブを順番に実行します。

```yaml
jobs:
  job1:
    overrides:
      params:
        simple_contextual_params:
          string_to_replace_with: "2028" # job1ではこの値を使用
  job2:
    overrides:
      workflow: # job2ではこのワークフローを適用
        - function: "multi_replace_from_lists"
          param_set: "multi_word_replace_params"
```

## 実行方法

1.  `PyReplacer` ディレクトリに `config.yaml` を配置します。
2.  入力ファイルを準備します。
3.  プロジェクトのルートディレクトリ（`PublicBox`）から、以下のコマンドを実行します。

    ```bash
    python3 -m PyReplacer.src.runner
    ```