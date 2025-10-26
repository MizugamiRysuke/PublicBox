import os
import re

def replace_string_contextual(text_content, string_to_find, string_to_replace_with, left_context_length=0, right_context_length=0):
    """
    指定文字列、およびオプションでその左右の文脈を含めて置換します。
    re.finditer を使用して、より明示的に置換を制御します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find (str): 検索するキーワード文字列。
        string_to_replace_with (str): 置換後の文字列。
        left_context_length (int, optional): キーワードの左側で置換に含める最大文字数。 Defaults to 0.
        right_context_length (int, optional): キーワードの右側で置換に含める最大文字数。 Defaults to 0.

    Returns:
        str: 置換後のテキスト。
    """
    pattern = re.compile(re.escape(string_to_find))
    result = []
    last_end = 0
    
    for match in pattern.finditer(text_content):
        match_start, match_end = match.span()
        
        # このマッチが前の置換の範囲内にある場合はスキップ
        if match_start < last_end:
            continue
            
        # 置換範囲の実際の開始位置と終了位置を決定
        replace_start = max(0, match_start - left_context_length)
        replace_end = min(len(text_content), match_end + right_context_length)
        
        # 置換前のテキスト部分を追加
        result.append(text_content[last_end:replace_start])
        
        # 置換文字列を追加
        result.append(string_to_replace_with)
        
        # 最後の終了位置を更新
        last_end = replace_end
        
    # 残りのテキストを追加
    result.append(text_content[last_end:])
    
    return "".join(result)

def execute_contextual_replacement(input_path, output_path, find_str, replacement_str, left_len=0, right_len=0):
    """
    ファイルを読み込み、文脈付き置換を実行し、結果を別ファイルに書き出します。
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

    replaced_text = replace_string_contextual(original_text, find_str, replacement_str, left_len, right_len)

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
            f.write("これは重要なキーワードを含むテキストです。キーワードの周りの文字も置換されます。")

    # 1. 単純置換のテスト
    execute_contextual_replacement(
        input_path=test_input_file,
        output_path="output_contextual_simple.txt",
        find_str="キーワード",
        replacement_str="【KEYWORD】"
    )

    # 2. 左文脈付き置換のテスト
    execute_contextual_replacement(
        input_path=test_input_file,
        output_path="output_contextual_left.txt",
        find_str="キーワード",
        replacement_str="【IMPORTANT_KEYWORD】",
        left_len=5
    )

    # 3. 右文脈付き置換のテスト
    execute_contextual_replacement(
        input_path=test_input_file,
        output_path="output_contextual_right.txt",
        find_str="キーワード",
        replacement_str="【KEYWORD_PROCESSED】",
        right_len=7
    )
    
    # 4. 左右両方の文脈付き置換のテスト
    execute_contextual_replacement(
        input_path=test_input_file,
        output_path="output_contextual_both.txt",
        find_str="キーワード",
        replacement_str="【PROCESSED】",
        left_len=5,
        right_len=7
    )

    print("\nスクリプトの直接実行によるテストが完了しました。")