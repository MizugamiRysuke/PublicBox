import unittest
import os
import sys

# srcディレクトリをsys.pathに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from text_replacer_ultimate import replace_ultimate

class TestTextReplacerUltimate(unittest.TestCase):

    def setUp(self):
        self.test_text = "ignore_これは前文です。[重要]この部分は中身です。[/重要]これが後文です。_ignore"

    def test_rearrange_all_parts(self):
        """全てのパーツを再配置するテスト"""
        result = replace_ultimate(
            text_content=self.test_text,
            left_context_len=8,         # 「これは前文です。」
            string_to_find_1="[重要]",
            middle_min_len=10,
            middle_max_len=15,
            string_to_find_2="[/重要]",
            right_context_len=8,        # 「これが後文です。」
            replacement_format_string=r"【中身】\3【文脈】(\1) (\5)【タグ】\2 \4"
        )
        expected = "ignore_【中身】この部分は中身です。【文脈】(これは前文です。) (これが後文です。)【タグ】[重要] [/重要]_ignore"
        self.assertEqual(result, expected)

    def test_replace_context_part(self):
        """文脈の一部を置換するテスト"""
        result = replace_ultimate(
            text_content=self.test_text,
            left_context_len=8,
            string_to_find_1="[重要]",
            middle_min_len=10,
            middle_max_len=15,
            string_to_find_2="[/重要]",
            right_context_len=8,
            replacement_format_string=r"【新しい前文】\2\3\4\5"
        )
        expected = "ignore_【新しい前文】[重要]この部分は中身です。[/重要]これが後文です。_ignore"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
