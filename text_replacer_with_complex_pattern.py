import os
import re

def replace_complex_pattern(text_content, string_to_find_1, string_to_find_2, string_to_replace_with, min_len=3, max_len=None):
    """
    「文字列1 + 任意のN文字 + 文字列2」のパターンにマッチした場合に置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find_1 (str): 検索パターンの開始文字列。
        string_to_find_2 (str): 検索パターンの終了文字列。
        string_to_replace_with (str): 置換後の文字列。
        min_len (int, optional): 間にある文字の最小長。max_lenがなければ固定長。 Defaults to 3.
        max_len (int, optional): 間にある文字の最大長。指定すると範囲指定になる。 Defaults to None.

    Returns:
        str: 置換後のテキスト。
    """
    if max_len is not None:
        # 範囲指定の場合: .{3,5}
        length_pattern = f"{{{min_len},{max_len}}}"
    else:
        # 固定長の場合: .{3}
        length_pattern = f"{{{min_len}}}"

    pattern_str = re.escape(string_to_find_1) + r"." + length_pattern + re.escape(string_to_find_2)
    pattern = re.compile(pattern_str)

    return pattern.sub(string_to_replace_with, text_content)

def execute_replacement(input_path, output_path, find_str1, find_str2, replacement_str, min_len=3, max_len=None):
    """
    ファイルを読み込み、複雑なパターン置換を実行し、結果を別ファイルに書き出します。
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

    replaced_text = replace_complex_pattern(original_text, find_str1, find_str2, replacement_str, min_len, max_len)

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
            f.write("これは開始...終了というパターンと、開始.....終了というパターンを含みます。")

    # 3～5文字の範囲指定でテスト
    success = execute_replacement(
        input_path=test_input_file,
        output_path="output_replaced_with_complex_pattern.txt",
        find_str1="開始",
        find_str2="終了",
        replacement_str="置換済みパターン",
        min_len=3,
        max_len=5
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")