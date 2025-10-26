# =================================================================
# PyReplacer 実行エンジン (runner.py)
#
# このスクリプトは、config.yaml を読み込み、
# 定義されたワークフローに従ってテキスト処理を実行します。
# =================================================================

import os
import yaml
import copy

# 1. 利用するライブラリ関数をすべてインポートする
# -----------------------------------------------------------------
from .text_replacer_with_sequence import replace_string_with_sequence
from .text_replacer_with_complex_pattern import replace_complex_pattern
from .text_replacer_from_list import replace_string_from_list
from .text_replacer_with_count_based_list import replace_string_with_count_based_list
from .text_multi_replacer_from_lists import multi_replace_from_lists
from .text_replacer_contextual import replace_string_contextual
from .text_replacer_ultimate import replace_ultimate

# 2. 文字列名と関数オブジェクトを対応付ける辞書
# -----------------------------------------------------------------
# config.yaml の "function" 文字列と、実際の関数をここで紐付けます。
# 新しいライブラリを追加した場合は、ここにも登録します。
AVAILABLE_FUNCTIONS = {
    "replace_string_with_sequence": replace_string_with_sequence,
    "replace_complex_pattern": replace_complex_pattern,
    "replace_string_from_list": replace_string_from_list,
    "replace_string_with_count_based_list": replace_string_with_count_based_list,
    "multi_replace_from_lists": multi_replace_from_lists,
    "replace_string_contextual": replace_string_contextual,
    "replace_ultimate": replace_ultimate,
}

# 3. ワークフロー実行ヘルパー関数
# -----------------------------------------------------------------
def run_workflow(text_content, workflow, params_definitions, output_path):
    """
    与えられたテキストに対し、指定されたワークフローを実行し、結果をファイルに書き出します。

    Args:
        text_content (str): 処理対象の初期テキスト。
        workflow (list): 実行するタスクのリスト。
        params_definitions (dict): パラメータセットの定義。
        output_path (str): 結果を書き出すファイルのパス。

    Returns:
        bool: 成功した場合はTrue。
    """
    processed_text = text_content

    print("--- ワークフロー開始 ---")
    for i, task in enumerate(workflow):
        print(f"  - ステップ {i+1}: を実行中...")
        
        func_name = task.get("function")
        param_set_name = task.get("param_set")

        if not (func_name and param_set_name):
            print(f"    警告: 'function' または 'param_set' が未定義です。スキップします。")
            continue

        params = params_definitions.get(param_set_name)
        if params is None:
            print(f"    警告: パラメータセット '{param_set_name}' が未定義です。スキップします。")
            continue

        print(f"    - 関数: {func_name}")
        print(f"    - パラメータセット: {param_set_name}")

        if func_name in AVAILABLE_FUNCTIONS:
            target_function = AVAILABLE_FUNCTIONS[func_name]
            processed_text = target_function(processed_text, **params)
        else:
            print(f"    警告: 関数 '{func_name}' が未定義です。スキップします。")

    print("\n--- ワークフロー完了後の最終結果 ---")
    print(processed_text)
    print("=" * 30)

    print(f"最終結果を '{output_path}' に書き込みます...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(processed_text)

    print(f"'{output_path}' への書き込みが完了しました。")
    return True

# 4. メイン処理エンジン
# -----------------------------------------------------------------
def main():
    """
    config.yaml を読み込み、定義されたジョブまたは単一ワークフローを実行します。
    """
    config_path = "../config.yaml"

    # --- 設定ファイルの読み込み ---
    print(f"'{config_path}' を読み込みます...")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"エラー: 設定ファイル '{config_path}' が見つかりません。")
        return
    except yaml.YAMLError as e:
        print(f"エラー: 設定ファイル '{config_path}' の解析に失敗しました。: {e}")
        return

    # --- ベース設定の取得 ---
    base_io = config.get("io", {})
    base_params = config.get("params", {})
    base_workflow = config.get("workflow", [])
    jobs = config.get("jobs")

    # --- 入力ファイルの読み込み ---
    input_path = os.path.join("..", base_io.get("input_path", "input.txt"))
    print(f"入力ファイル '{input_path}' を読み込みます...")
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            initial_text = f.read()
    except FileNotFoundError:
        if input_path == os.path.join("..", "sample_input.txt"):
            print(f"'{input_path}' が見つからないため、サンプルを生成します。")
            initial_text = """# テスト用総合入力ファイル

## フルーツリスト
- APPLE
- ORANGE
- APPLE
- ORANGE
- APPLE

## ノート
ITEM: これは重要なキーワードです。
ITEM: これもキーワードです。
ITEM: これもキーワードです。

## パターン
これは開始...終了というパターンです。

## カウントベース
COUNT_TARGET COUNT_TARGET COUNT_TARGET COUNT_TARGET COUNT_TARGET

## リスト置換
LIST_REPLACE LIST_REPLACE LIST_REPLACE LIST_REPLACE LIST_REPLACE

## フッター
(C) 2025 My Memo"""
            with open(input_path, "w", encoding="utf-8") as f_write:
                f_write.write(initial_text)
        else:
            print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
            return

    # --- 実行モードの分岐 ---
    if jobs:
        # --- 複数ジョブ実行モード ---
        print(f"\n{len(jobs)}個のジョブを実行します。")
        print("=" * 40)
        
        for job_name, job_config in jobs.items():
            print(f"ジョブ '{job_name}' を開始します...")
            
            current_params = copy.deepcopy(base_params)
            current_workflow = copy.deepcopy(base_workflow)
            
            overrides = job_config.get("overrides", {})
            
            override_params = overrides.get("params", {})
            for param_set_name, new_values in override_params.items():
                if param_set_name in current_params:
                    current_params[param_set_name].update(new_values)

            if "workflow" in overrides:
                current_workflow = overrides["workflow"]
            
            output_path = os.path.join("..", base_io.get("output_path", "output.txt").format(job_name=job_name))
            
            print("--- 元のテキスト ---")
            print(initial_text)
            
            run_workflow(initial_text, current_workflow, current_params, output_path)
            print(f"ジョブ '{job_name}' が完了しました。")
            print("-" * 40)

    else:
        # --- 単一実行モード ---
        print("\n単一実行モードで実行します。")
        output_path = os.path.join("..", base_io.get("output_path", "output.txt").format(job_name="single"))
        print("--- 元のテキスト ---")
        print(initial_text)
        run_workflow(initial_text, base_workflow, base_params, output_path)

# 5. スクリプト実行のエントリーポイント
# -----------------------------------------------------------------
if __name__ == "__main__":
    # このスクリプトがあるディレクトリを基準に動作するようカレントディレクトリを変更
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()