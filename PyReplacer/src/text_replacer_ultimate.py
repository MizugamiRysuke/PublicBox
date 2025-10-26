import os
import re

def replace_ultimate(text_content, replacement_format_string, left_context_len=0, string_to_find_1=None, middle_min_len=0, middle_max_len=None, string_to_find_2=None, right_context_len=0):
    """
    究極の置換機能：5つのパートをキャプチャし、フォーマット文字列に基づいて自由に置換します。

    Args:
        text_content (str): 処理対象のテキスト。
        replacement_format_string (str): 置換フォーマット文字列。\1から\5までの後方参照を使用できます。
        left_context_len (int): 左文脈の長さ。
        string_to_find_1 (str, optional): 検索文字列1。
        middle_min_len (int): 中間部分の最小長。
        middle_max_len (int, optional): 中間部分の最大長。
        string_to_find_2 (str, optional): 検索文字列2。
        right_context_len (int): 右文脈の長さ。

    Returns:
        str: 置換後のテキスト。
    """
    # 各パートの正規表現パターンを構築
    p1 = f'(.{{{left_context_len}}})' if left_context_len > 0 else '()'
    p2 = f'({re.escape(string_to_find_1)})' if string_to_find_1 else '()'
    
    if middle_max_len is not None:
        middle_len_pattern = f'{{{middle_min_len},{middle_max_len}}}'
    else:
        middle_len_pattern = f'{{{middle_min_len},}}' # max_lenがなければmin_len以上
    
    # p3は指定された長さで、非貪欲にマッチする
    p3 = f'(.{middle_len_pattern}?)'

    p4 = f'({re.escape(string_to_find_2)})' if string_to_find_2 else '()'
    p5 = f'(.{{{right_context_len}}})' if right_context_len > 0 else '()'

    # 5つのグループを持つ最終的なパターン
    full_pattern = re.compile(p1 + p2 + p3 + p4 + p5)

    return full_pattern.sub(replacement_format_string, text_content)

if __name__ == '__main__':
    """
    このスクリプトが直接実行された場合に、テストとして上記の関数を呼び出します。
    """
    test_text = "ignore_これは前文です。[重要]この部分は中身です。[/重要]これが後文です。_ignore"
    
    # --- テストケース1: 全てのパーツを再配置 ---
    result1 = replace_ultimate(
        text_content=test_text,
        left_context_len=8,         # 「これは前文です。」
        string_to_find_1="[重要]",
        middle_min_len=10,          # 「この部分は中身です。」
        middle_max_len=15,
        string_to_find_2="[/重要]",
        right_context_len=8,        # 「これが後文です。」
        # \3(中身)を先頭に、\1(前文)と\5(後文)を括弧で囲み、\2と\4(タグ)を最後に表示
        replacement_format_string=r"【中身】\3【文脈】(\1) (\5)【タグ】\2 \4"
    )
    print("--- テスト1 結果 ---")
    print(result1)
    print("期待値: ignore_【中身】この部分は中身です。【文脈】(これは前文です。) (これが後文です。)【タグ】[重要] [/重要]_ignore")

    # --- テストケース2: 文脈の一部を置換 ---
    result2 = replace_ultimate(
        text_content=test_text,
        left_context_len=8,
        string_to_find_1="[重要]",
        middle_min_len=10,
        middle_max_len=15,
        string_to_find_2="[/重要]",
        right_context_len=8,
        # \1(左文脈)を新しい文字列に置き換え、他はそのまま
        replacement_format_string=r"【新しい前文】\2\3\4\5"
    )
    print("\n--- テスト2 結果 ---")
    print(result2)
    print("期待値: ignore_【新しい前文】[重要]この部分は中身です。[/重要]これが後文です。_ignore")
