import os
import re

def replace_string_from_list(text_content, string_to_find, replacement_list, loop=False):
    """
    テキスト内の指定文字列を、リストの要素で順番に置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find (str): 検索する文字列。
        replacement_list (list): 置換に使用する文字列のリスト。
        loop (bool, optional): リストを循環して使用するか。 Defaults to False.

    Returns:
        str: 置換後のテキスト。
    """
    list_index = 0
    list_length = len(replacement_list)
    if list_length == 0:
        return text_content # 置換リストが空なら何もしない

    # 置換関数
    def replacer(match):
        nonlocal list_index
        
        if loop:
            # 剰余演算子(%)を使ってインデックスを循環させる
            current_replacement = replacement_list[list_index % list_length]
        else:
            # 従来通り、リストの末尾の要素を使い続ける
            current_replacement = replacement_list[min(list_index, list_length - 1)]
        
        list_index += 1
        return current_replacement

    pattern = re.compile(re.escape(string_to_find))
    return pattern.sub(replacer, text_content)

def execute_replacement_from_list(input_path, output_path, find_str, replacement_values, loop=False):
    """
    ファイルを読み込み、リストに基づいて置換を実行し、結果を別ファイルに書き出します。
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
    replaced_text = replace_string_from_list(original_text, find_str, replacement_values, loop)

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
            f.write("置換対象 " * 5) # ループをテストするために5回繰り返す

    test_replacement_values = ["りんご", "バナナ", "みかん"]

    success = execute_replacement_from_list(
        input_path=test_input_file,
        output_path="output_replaced_from_list.txt",
        find_str="置換対象",
        replacement_values=test_replacement_values,
        loop=True # ループ機能をテスト
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")
