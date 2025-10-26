import os
import re

def multi_replace_from_lists(text_content, replacement_rules, loop_lists=False):
    """
    複数の置換ルールに基づきテキストを置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        replacement_rules (list): 置換ルールのリスト。
        loop_lists (bool, optional): 全てのルールでリストをループさせるかのデフォルト値。Defaults to False.

    Returns:
        str: 置換後のテキスト。
    
    Note:
        各ルール辞書内で "loop": True を指定すると、個別にループを有効にできます。
    """
    processed_text = text_content

    for rule in replacement_rules:
        string_to_find = rule["find_string"]
        replacement_list = rule.get("replacement_list", [])
        # ルール内で個別にループ指定があればそれを優先し、なければ全体の指定に従う
        should_loop = rule.get("loop", loop_lists)

        list_index = 0
        list_length = len(replacement_list)
        if list_length == 0:
            continue # 置換リストが空の場合はスキップ

        # 置換関数
        def replacer(match):
            nonlocal list_index
            
            if should_loop:
                # 剰余演算子(%)を使ってインデックスを循環させる
                current_replacement = replacement_list[list_index % list_length]
            else:
                # 従来通り、リストの末尾の要素を使い続ける
                current_replacement = replacement_list[min(list_index, list_length - 1)]
            
            list_index += 1
            return current_replacement

        pattern = re.compile(re.escape(string_to_find))
        processed_text = pattern.sub(replacer, processed_text)

    return processed_text

def execute_multi_replacement(input_path, output_path, replacement_rules, loop_lists=False):
    """
    ファイルを読み込み、複数の置換ルールに基づいて置換を実行し、結果を別ファイルに書き出します。
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
        return False

    print(f"--- 置換前テキスト ({input_path}) ---")
    print(original_text)
    print("-" * 30)

    # 修正した中核関数を呼び出す
    replaced_text = multi_replace_from_lists(original_text, replacement_rules, loop_lists)

    print(f"--- 置換後テキスト ({output_path}) ---")
    print(replaced_text)
    print("-" * 30)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(replaced_text)

    print(f"置換後のテキストが '{output_path}' に出力されました。")
    return True

if __name__ == "__main__":
    """
    このスクリプトが直接実行された場合に、テストとして上記の関数を呼び出します。
    """
    test_input_file = "input.txt"
    if not os.path.exists(test_input_file):
        print(f"テスト用の '{test_input_file}' が見つからないため、新規作成します。")
        with open(test_input_file, "w", encoding="utf-8") as f:
            f.write("A, B, C, A, B, C, A, B, C")

    # テスト用の置換ルール
    test_rules = [
        {
            "find_string": "A",
            "replacement_list": ["Apple", "Avocado"],
            "loop": True  # この「A」のルールだけループさせる
        },
        {
            "find_string": "B",
            "replacement_list": ["Banana", "Blueberry"]
            # loopの指定がないので、全体のloop_lists設定(デフォルトはFalse)に従う
        },
        {
            "find_string": "C",
            "replacement_list": ["Cherry"]
        }
    ]

    success = execute_multi_replacement(
        input_path=test_input_file,
        output_path="output_multi_replaced_from_lists.txt",
        replacement_rules=test_rules
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")
