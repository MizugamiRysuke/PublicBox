import unittest
import sys
import os

# 親ディレクトリ(toolcode)をPythonのパスに追加して、PyReplacerパッケージをインポートできるようにする
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyReplacer.text_replacer import replace_string_in_text

class TestSimpleReplacer(unittest.TestCase):
    """
    text_replacer.py のテストクラス
    """

    def test_simple_replacement(self):
        """基本的な置換が正しく行われるかテスト"""
        text = "Hello world, hello universe."
        old = "hello"
        new = "Hi"
        expected = "Hello world, Hi universe."
        result = replace_string_in_text(text, old, new)
        self.assertEqual(result, expected)

    def test_no_match(self):
        """置換対象が見つからない場合に、テキストが変わらないことをテスト"""
        text = "This is a test."
        old = "nonexistent"
        new = "replacement"
        expected = "This is a test."
        result = replace_string_in_text(text, old, new)
        self.assertEqual(result, expected)

    def test_empty_string_replacement(self):
        """空文字列への置換をテスト"""
        text = "Remove this word."
        old = " word"
        new = ""
        expected = "Remove this."
        result = replace_string_in_text(text, old, new)
        self.assertEqual(result, expected)

    def test_case_sensitive(self):
        """置換が大文字と小文字を区別することを確認"""
        text = "Hello hello Hello"
        old = "Hello"
        new = "Hi"
        expected = "Hi hello Hi"
        result = replace_string_in_text(text, old, new)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
