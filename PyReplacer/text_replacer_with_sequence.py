import os
import re

def replace_string_with_sequence(text_content, string_to_find, start_number=1, format_string="[{}]"):
    """
    テキスト内の指定文字列を、見つけるたびに連番に置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        string_to_find (str): 検索する文字列。
        start_number (int, optional): 連番の開始番号。 Defaults to 1.
        format_string (str, optional): 連番の書式。{}が番号に置換されます。 Defaults to "[{}]".

    Returns:
        str: 置換後のテキスト。
    """
    counter = start_number - 1

    # 置換関数
    def replacer(match):
        nonlocal counter
        counter += 1
        return format_string.format(counter)

    # re.escape() を使用して、string_to_find が正規表現の特殊文字を含んでいても正しく動作するようにします。
    pattern = re.compile(re.escape(string_to_find))

    return pattern.sub(replacer, text_content)

# --- ここからが新しい関数 ---
def execute_replacement_with_sequence(input_path, output_path, find_str, start_num=1, fmt_str="[{}]"):
    """
    ファイルを読み込み、連番置換を実行し、結果を別ファイルに書き出します。
    他のPythonスクリプトから呼び出すためのメインの関数です。

    Args:
        input_path (str): 入力ファイルのパス
        output_path (str): 出力ファイルのパス
        find_str (str): 検索する文字列
        start_num (int, optional): 連番の開始番号. Defaults to 1.
        fmt_str (str, optional): 連番のフォーマット文字列. '{}'が番号に置換される. Defaults to "[{}]".

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
    replaced_text = replace_string_with_sequence(original_text, find_str, start_num, fmt_str)

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
            f.write("これは置換対象のテキストです。置換対象が複数あります。置換対象、置換対象。")

    # 作成した関数を呼び出す
    success = execute_replacement_with_sequence(
        input_path=test_input_file,
        output_path="output_replaced_with_sequence.txt",
        find_str="置換対象",
        start_num=101, # テスト用に開始番号を101にしてみる
        fmt_str="Item-No.{}" # テスト用にフォーマットを変更してみる
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")