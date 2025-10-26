import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyReplacer.text_replacer_with_count_based_list import replace_string_with_count_based_list

class TestCountBasedReplacer(unittest.TestCase):
    def test_count_based_replacement(self):
        """回数ベースの置換をテスト"""
        text = "A " * 10
        find = "A"
        rules = [("B", 3), ("C", 7), ("D", 10)]
        # 1-3 -> B, 4-7 -> C, 8-10 -> D
        expected = "B B B C C C C D D D "
        result = replace_string_with_count_based_list(text, find, rules)
        self.assertEqual(result, expected)

    def test_last_rule_continues(self):
        """最後のルールが継続されるかテスト"""
        text = "A " * 5
        find = "A"
        rules = [("B", 2), ("C", 3)]
        # 1-2 -> B, 3以降 -> C
        expected = "B B C C C "
        result = replace_string_with_count_based_list(text, find, rules)
        self.assertEqual(result, expected)
