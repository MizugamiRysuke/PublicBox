import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyReplacer.text_multi_replacer_from_lists import multi_replace_from_lists

class TestMultiListReplacer(unittest.TestCase):
    def test_multiple_rules(self):
        """複数のルールが正しく適用されるかテスト"""
        text = "A and B. A again."
        rules = [
            {"find_string": "A", "replacement_list": ["Apple", "Avocado"]},
            {"find_string": "B", "replacement_list": ["Banana"]}
        ]
        expected = "Apple and Banana. Avocado again."
        result = multi_replace_from_lists(text, rules)
        self.assertEqual(result, expected)

    def test_looping_and_non_looping_rules(self):
        """ループするルールとしないルールが共存するケースをテスト"""
        text = "A, B, A, B, A, B"
        rules = [
            {"find_string": "A", "replacement_list": ["1", "2"], "loop": True},
            {"find_string": "B", "replacement_list": ["x", "y"], "loop": False}
        ]
        expected = "1, x, 2, y, 1, y"
        result = multi_replace_from_lists(text, rules)
        self.assertEqual(result, expected)

    def test_global_loop_setting(self):
        """全体のループ設定が適用されるかテスト"""
        text = "A, B, A, B, A, B"
        rules = [
            {"find_string": "A", "replacement_list": ["1", "2"]},
            {"find_string": "B", "replacement_list": ["x", "y"]}
        ]
        expected = "1, x, 2, y, 1, x"
        # loop_lists=True をグローバルに設定
        result = multi_replace_from_lists(text, rules, loop_lists=True)
        self.assertEqual(result, expected)
