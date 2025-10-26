import os

def replace_string_in_text(text_content, old_string, new_string):
    """
    テキスト内の指定された文字列を、すべて別の文字列に置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        old_string (str): 検索する文字列。
        new_string (str): 置換後の文字列。

    Returns:
        str: 置換後のテキスト。
    """
    return text_content.replace(old_string, new_string)

# --- ここからが新しい関数 ---
def execute_simple_replacement(input_path, output_path, old_str, new_str):
    """
    ファイルを読み込み、単純な文字列置換を実行し、結果を別ファイルに書き出します。
    他のPythonスクリプトから呼び出すためのメインの関数です。

    Args:
        input_path (str): 入力ファイルのパス
        output_path (str): 出力ファイルのパス
        old_str (str): 検索する文字列
        new_str (str): 置換後の文字列

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
    replaced_text = replace_string_in_text(original_text, old_str, new_str)

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
            f.write("これは古い文字列を含むテキストです。古い文字列は、本当に古いです。")

    # 作成した関数を呼び出す
    success = execute_simple_replacement(
        input_path=test_input_file,
        output_path="output_replaced.txt",
        old_str="古い文字列",
        new_str="新しい文字列"
    )

    if success:
        print("\nスクリプトの直接実行によるテストが完了しました。")
    else:
        print("\nスクリプトの直接実行によるテスト中にエラーが発生しました。")