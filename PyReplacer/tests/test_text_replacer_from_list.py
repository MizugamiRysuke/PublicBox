import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyReplacer.text_replacer_from_list import replace_string_from_list

class TestListReplacer(unittest.TestCase):
    """
    text_replacer_from_list.py のテストクラス
    """

    def test_sequential_replacement_no_loop(self):
        """基本的な順次置換（ループなし）をテスト"""
        text = "A, A, A, A"
        find = "A"
        replacements = ["B", "C", "D"]
        # ループしないので、最後は "D" が使われ続ける
        expected = "B, C, D, D"
        result = replace_string_from_list(text, find, replacements, loop=False)
        self.assertEqual(result, expected)

    def test_sequential_replacement_with_loop(self):
        """ループを有効にした場合の順次置換をテスト"""
        text = "A, A, A, A"
        find = "A"
        replacements = ["B", "C", "D"]
        # ループするので、4つ目は先頭の "B" に戻る
        expected = "B, C, D, B"
        result = replace_string_from_list(text, find, replacements, loop=True)
        self.assertEqual(result, expected)

    def test_default_no_loop(self):
        """ループ引数未指定時（デフォルト=False）の動作をテスト"""
        text = "A, A, A, A"
        find = "A"
        replacements = ["B", "C", "D"]
        expected = "B, C, D, D"
        # loop引数を指定しない
        result = replace_string_from_list(text, find, replacements)
        self.assertEqual(result, expected)

    def test_list_longer_than_matches(self):
        """置換リストの方が長い場合のテスト"""
        text = "A, A"
        find = "A"
        replacements = ["B", "C", "D", "E"]
        expected = "B, C"
        result = replace_string_from_list(text, find, replacements)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
