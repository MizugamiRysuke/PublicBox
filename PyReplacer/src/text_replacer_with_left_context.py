import os
import re

def replace_string_with_left_context(text_content, string_to_find, string_to_replace_with, context_length=3):
    """
    指定文字列と、それに先行する指定長の文字列をまとめて置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find (str): 検索するキーワード文字列。
        string_to_replace_with (str): 置換後の文字列。
        context_length (int, optional): キーワードの左側で置換に含める最大文字数。 Defaults to 3.

    Returns:
        str: 置換後のテキスト。
    """
    # string_to_find の前に続く最大 context_length 文字をキャプチャする正規表現パターン
    # re.escape() を使用して、string_to_find が正規表現の特殊文字を含んでいても正しく動作するようにします。
    pattern = re.compile(r"(.{0," + str(context_length) + r"})" + re.escape(string_to_find))

    # 置換関数
    def replacer(match):
        # マッチした部分全体を string_to_replace_with で置き換える
        return string_to_replace_with

    return pattern.sub(replacer, text_content)

# --- ここからが新しい関数 ---
def execute_replacement_with_left_context(input_path, output_path, find_str, replacement_str, left_context_length=3):
    """
    ファイルを読み込み、左側の文脈を含めて置換を実行し、結果を別ファイルに書き出します。
    他のPythonスクリプトから呼び出すためのメインの関数です。

    Args:
        input_path (str): 入力ファイルのパス
        output_path (str): 出力ファイルのパス
        find_str (str): 検索するキーワード文字列
        replacement_str (str): 置換後の文字列
        left_context_length (int, optional): キーワードの左側で置換に含める最大文字数. Defaults to 3.

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

    # 置換関数を呼び出す
    replaced_text = replace_string_with_left_context(original_text, find_str, replacement_str, left_context_length)

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
            f.write("これは重要なキーワードを含むテキストです。キーワードの前に続く文字も置換されます。")

    # 作成した関数を呼び出す
    success = execute_replacement_with_left_context(
        input_path=test_input_file,
        output_path="output_replaced_with_left_context.txt",
        find_str="キーワード",
        replacement_str="置換済み",
        left_context_length=5 # テスト用に文脈長を5にしてみる
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")