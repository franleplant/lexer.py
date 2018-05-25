import unittest
from main import lex


class TestLex(unittest.TestCase):

    def test_one(self):
        src = ' if'
        error, actual_tokens = lex(src)
        expected_tokens = [ ('If', 'if', 1, 2) ]

        self.assertEqual(actual_tokens, expected_tokens)

    def test_integration_one(self):
        src = '  if { 123 {{ {123 if{'
        error, actual_tokens = lex(src)
        expected_tokens = [
            ('If', 'if', 1, 3),
            ('{', '{', 1, 6),
            ('Number', '123', 1, 8),
            ('{', '{', 1, 12),
            ('{', '{', 1, 13),
            ('{', '{', 1, 15),
            ('Number', '123', 1, 16),
            ('If', 'if', 1 , 20),
            ('{', '{', 1 , 22)
        ]

        self.assertEqual(actual_tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
