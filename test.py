import unittest
from main import lex


class TestLex(unittest.TestCase):

    def test_one(self):
        src = '  if { 123 {{ {123 if{'
        actual_tokens = lex(src)
        expected_tokens = [
            ('If', 'if'),
            ('{', '{'),
            ('{', '{'),
            ('{', '{'),
            ('Number', 123),
            ('If', 'if'),
            ('{', '{')
        ]

        self.assertEqual(actual_tokens, expected_tokens)



if __name__ == '__main__':
    unittest.main()
