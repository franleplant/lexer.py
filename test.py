import unittest
from main import lex


class TestLex(unittest.TestCase):

    def test_one(self):
        src = ' if'
        actual_tokens = lex(src)
        expected_tokens = [ ('IF', 'if', 1, 2) ]

        self.assertEqual(actual_tokens, expected_tokens)

    def test_integration_one(self):
        src = '  if { 123 {{ {123 if{'
        actual_tokens = lex(src)
        expected_tokens = [
            ('IF', 'if', 1, 3),
            ('CURLY_OPEN', '{', 1, 6),
            ('NUM', '123', 1, 8),
            ('CURLY_OPEN', '{', 1, 12),
            ('CURLY_OPEN', '{', 1, 13),
            ('CURLY_OPEN', '{', 1, 15),
            ('NUM', '123', 1, 16),
            ('IF', 'if', 1 , 20),
            ('CURLY_OPEN', '{', 1 , 22)
        ]

        self.assertEqual(actual_tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
