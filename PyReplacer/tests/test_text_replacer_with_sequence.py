import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_replacer_with_sequence import replace_string_with_sequence

class TestSequenceReplacer(unittest.TestCase):
    """
    text_replacer_with_sequence.py のテストクラス
    """

    def test_basic_sequence(self):
        """基本的な連番置換をテスト"""
        text = "A, A, A"
        find = "A"
        expected = "[1], [2], [3]"
        result = replace_string_with_sequence(text, find)
        self.assertEqual(result, expected)

    def test_custom_start_number(self):
        """開始番号の指定をテスト"""
        text = "A, A, A"
        find = "A"
        expected = "[101], [102], [103]"
        result = replace_string_with_sequence(text, find, start_number=101)
        self.assertEqual(result, expected)

    def test_custom_format(self):
        """フォーマットの指定をテスト"""
        text = "A, A"
        find = "A"
        expected = "No.1, No.2"
        result = replace_string_with_sequence(text, find, format_string="No.{}")
        self.assertEqual(result, expected)

    def test_no_match(self):
        """マッチしない場合のテスト"""
        text = "B, C, D"
        find = "A"
        expected = "B, C, D"
        result = replace_string_with_sequence(text, find)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
