import os
import re

def replace_string_with_count_based_list(text_content, string_to_find, replacement_rules):
    """
    指定文字列を、出現回数に応じたルールで置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find (str): 検索する文字列。
        replacement_rules (list): 置換ルールのリスト。
                                  各ルールは (置換文字列, 適用する最後の回数) のタプル。

    Returns:
        str: 置換後のテキスト。
    """
    current_find_count = 0
    rule_index = 0
    
    # 置換関数
    def replacer(match):
        nonlocal current_find_count
        nonlocal rule_index
        
        current_find_count += 1
        
        # 現在のルールが適用回数に達しているか確認
        while rule_index < len(replacement_rules) - 1 and \
              current_find_count > replacement_rules[rule_index][1]:
            rule_index += 1
            
        # 現在のルールから置き換え文字列を取得
        return replacement_rules[rule_index][0]

    # re.escape() を使用して、string_to_find が正規表現の特殊文字を含んでいても正しく動作するようにします。
    pattern = re.compile(re.escape(string_to_find))

    return pattern.sub(replacer, text_content)

# --- ここからが新しい関数 ---
def execute_replacement_with_count_based_list(input_path, output_path, find_str, rules):
    """
    ファイルを読み込み、出現回数
    に基づいたリスト置換を実行し、結果を別ファイルに書き出します。
    他のPythonスクリプトから呼び出すためのメインの関数です。

    Args:
        input_path (str): 入力ファイルのパス
        output_path (str): 出力ファイルのパス
        find_str (str): 検索する文字列
        rules (list): 置換ルールのリスト。各ルールは (置換文字列, 適用する最後の回数) のタプル。

    Returns:
        bool: 処理が成功した場合は True、失敗した場合は False
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

    # 既存の置換関数を呼び出す
    replaced_text = replace_string_with_count_based_list(original_text, find_str, rules)

    print(f"--- 置換後テキスト ({output_path}) ---")
    print(replaced_text)
    print("-" * 30)

    # 置換後の内容をファイルに出力
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(replaced_text)

    print(f"置換後のテキストが '{output_path}' に出力されました。")
    return True


# --- ここからが新しい __main__ ブロック ---
if __name__ == "__main__":
    """
    このスクリプトが直接実行された場合に、テストとして上記の関数を呼び出します。
    """
    # テスト用の入力ファイル名
    test_input_file = "input.txt"

    # 入力ファイルが存在しない場合は、テスト用に作成する
    if not os.path.exists(test_input_file):
        print(f"テスト用の '{test_input_file}' が見つからないため、新規作成します。")
        with open(test_input_file, "w", encoding="utf-8") as f:
            f.write("置換対象 " * 10) # 10個の置換対象を書き込む

    # テスト用の置換ルール
    test_rules = [
        ("Apple", 3),   # 1回目から3回目までApple
        ("Banana", 7),  # 4回目から7回目までBanana
        ("Cherry", 9)   # 8回目から9回目までCherry (10回目以降もCherry)
    ]

    # 作成した関数を呼び出す
    success = execute_replacement_with_count_based_list(
        input_path=test_input_file,
        output_path="output_replaced_with_count_based_list.txt",
        find_str="置換対象",
        rules=test_rules
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")