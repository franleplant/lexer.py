import unittest
from main import lex


class TestLex(unittest.TestCase):
    def test_one(self):
        src = ' if'
        error, actual_tokens = lex(src)
        expected_tokens = [('If', 'if', 1, 2)]

        self.assertEqual(actual_tokens, expected_tokens)
        # for (actual, expected) in zip(actual_tokens, expected_tokens):
        # self.assertEqual(actual, expected)
        # self.assertEqual(actual.kind, expected[0])
        # self.assertEqual(actual.lexeme, expected[1])
        # self.assertEqual(actual.line, expected[2])
        # self.assertEqual(actual.col, expected[3])

    def test_integration_one(self):
        src = '  if { 123 {{ {123 if{'
        error, actual_tokens = lex(src)
        expected_tokens = [('If', 'if', 1, 3), ('{', '{', 1, 6),
                           ('Number', 123, 1, 8), ('{', '{', 1, 12), ('{', '{',
                                                                      1, 13),
                           ('{', '{', 1, 15), ('Number', 123, 1,
                                               16), ('If', 'if', 1,
                                                     20), ('{', '{', 1, 22)]

        print(("suck", actual_tokens))

        self.assertEqual(actual_tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()
