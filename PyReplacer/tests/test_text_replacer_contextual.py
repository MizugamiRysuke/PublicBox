import unittest
import os
import sys

# srcディレクトリをsys.pathに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from text_replacer_contextual import replace_string_contextual

class TestTextReplacerContextual(unittest.TestCase):

    def setUp(self):
        """各テストの前に実行されるセットアップ"""
        self.base_text = "これは重要なキーワードを含むテキストです。キーワードの周りの文字も置換されます。"

    def test_simple_replacement(self):
        """単純な置換をテスト"""
        replaced_text = replace_string_contextual(
            self.base_text, 
            string_to_find="キーワード", 
            string_to_replace_with="【KEYWORD】"
        )
        self.assertEqual(
            replaced_text, 
            "これは重要な【KEYWORD】を含むテキストです。【KEYWORD】の周りの文字も置換されます。"
        )

    def test_left_context_replacement(self):
        """左側の文脈を含む置換をテスト"""
        replaced_text = replace_string_contextual(
            self.base_text, 
            string_to_find="キーワード", 
            string_to_replace_with="【IMPORTANT_KEYWORD】",
            left_context_length=5
        )
        self.assertEqual(
            replaced_text, 
            "こ【IMPORTANT_KEYWORD】を含むテキ【IMPORTANT_KEYWORD】の周りの文字も置換されます。"
        )

    def test_right_context_replacement(self):
        """右側の文脈を含む置換をテスト"""
        replaced_text = replace_string_contextual(
            self.base_text, 
            string_to_find="キーワード", 
            string_to_replace_with="【KEYWORD_PROCESSED】",
            right_context_length=7
        )
        self.assertEqual(
            replaced_text, 
            "これは重要な【KEYWORD_PROCESSED】です。【KEYWORD_PROCESSED】置換されます。"
        )
        
    def test_both_context_replacement(self):
        """左右両方の文脈を含む置換をテスト"""
        replaced_text = replace_string_contextual(
            self.base_text, 
            string_to_find="キーワード", 
            string_to_replace_with="【PROCESSED】",
            left_context_length=5,
            right_context_length=7
        )
        self.assertEqual(
            replaced_text, 
            "こ【PROCESSED】【PROCESSED】置換されます。"
        )

if __name__ == '__main__':
    unittest.main()
