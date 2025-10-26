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
    *   `text_replacer_ultimate.py`: 5つのパート（左文脈、文字列1、中間、文字列2、右文脈）をキャプチャし、自由に再配置・置換する究極の置換機能
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
  multi_word_replace_params:
    replacement_rules:
      - find_string: 'APPLE'
        replacement_list: ['りんご', '青りんご']

  # --- 連番に置換 ---
  sequence_replace_params:
    string_to_find: 'ITEM:'
    start_number: 1
    format_string: '項目{}:'

  # --- 文脈に応じて置換（統合版） ---
  simple_contextual_params:
    string_to_find: "2025"
    string_to_replace_with: "2026"

  # --- 究極の置換 ---
  # from: text_replacer_ultimate.py
  ultimate_replace_params:
    # \1: left_context_len で指定した左文脈
    left_context_len: 8
    # \2: string_to_find_1 で指定した文字列
    string_to_find_1: "[重要]"
    # \3: 中間文字列
    middle_min_len: 10
    middle_max_len: 15
    # \4: string_to_find_2 で指定した文字列
    string_to_find_2: "[/重要]"
    # \5: right_context_len で指定した右文脈
    right_context_len: 8
    # 置換フォーマット (YAML内では \1 のようにバックスラッシュを2つ重ねて記述します)
    replacement_format_string: "【中身】\3【文脈】(\1) (\5)【タグ】\2 \4"
```

### `workflow`

実行する置換処理のシーケンス（ワークフロー）をリストで定義します。各ステップでは、使用するモジュールと、`params` で定義したパラメータセットへの参照 (`param_set`) を指定します。

```yaml
workflow:
  - function: "replace_ultimate"
    param_set: "ultimate_replace_params"
  - function: "replace_string_contextual"
    param_set: "simple_contextual_params"
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
```

## 実行方法

1.  `PyReplacer` ディレクトリに `config.yaml` を配置します。
2.  入力ファイルを準備します。
3.  プロジェクトのルートディレクトリ（`PublicBox`）から、以下のコマンドを実行します。

    ```bash
    python3 -m PyReplacer.src.runner
    ```