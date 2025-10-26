import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyReplacer.text_replacer_with_left_context import replace_string_with_left_context

class TestLeftContextReplacer(unittest.TestCase):
    def test_basic_left_context(self):
        """基本的な左文脈置換をテスト"""
        text = "abcKEYWORD"
        find = "KEYWORD"
        replace_with = "REPLACED"
        expected = "REPLACED"
        # "abc"も一緒に置換される
        result = replace_string_with_left_context(text, find, replace_with, context_length=3)
        self.assertEqual(result, expected)

    def test_shorter_context(self):
        """文脈が指定より短い場合のテスト"""
        text = "abKEYWORD"
        find = "KEYWORD"
        replace_with = "REPLACED"
        expected = "REPLACED"
        result = replace_string_with_left_context(text, find, replace_with, context_length=3)
        self.assertEqual(result, expected)

    def test_no_context(self):
        """文脈が全くない場合（行頭）のテスト"""
        text = "KEYWORD"
        find = "KEYWORD"
        replace_with = "REPLACED"
        expected = "REPLACED"
        result = replace_string_with_left_context(text, find, replace_with, context_length=3)
        self.assertEqual(result, expected)
