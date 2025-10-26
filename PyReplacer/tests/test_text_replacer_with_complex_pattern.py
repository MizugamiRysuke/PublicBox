import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text_replacer_with_complex_pattern import replace_complex_pattern

class TestComplexPatternReplacer(unittest.TestCase):
    def test_fixed_length(self):
        """固定長でのパターン置換をテスト"""
        text = "start...end"
        expected = "REPLACED"
        result = replace_complex_pattern(text, "start", "end", "REPLACED", min_len=3)
        self.assertEqual(result, expected)

    def test_range_length_match(self):
        """範囲指定でマッチする場合のテスト"""
        text = "start....end" # 4文字
        expected = "REPLACED"
        result = replace_complex_pattern(text, "start", "end", "REPLACED", min_len=3, max_len=5)
        self.assertEqual(result, expected)

    def test_range_length_no_match(self):
        """範囲指定でマッチしない場合のテスト"""
        text = "start......end" # 6文字
        expected = "start......end"
        result = replace_complex_pattern(text, "start", "end", "REPLACED", min_len=3, max_len=5)
        self.assertEqual(result, expected)
