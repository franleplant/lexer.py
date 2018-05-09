from typing import cast, List, Tuple
import re

m = [
    ('{', re.compile('{').match),
    ('Number', re.compile('\d+').match),
]


class LexExcepction(Exception):
    pass


def lex(src: str) -> List[Tuple[str, str, int, int]]:
    tokens = []
    wordBegin = None
    for i in range(0, len(src) + 1):
        c = None
        if i < len(src):
            c = src[i]
        else:
            # Fake space at the end of the string
            c = ' '
        if wordBegin == None:
            # Trailing whitespace
            if c.isspace():
                continue
            # Word Begin
            else:
                wordBegin = i
        else:
            # Word End
            if c.isspace():
                wordEnd = i
                word = src[wordBegin:wordEnd]
                results = [
                    TokenKind for (TokenKind, matcher) in m if matcher(word)
                ]
                if len(results) == 0:
                    raise LexExcepction(
                        'Unrecognized Token in ' + str(wordBegin))
                token = (results[0], word, cast(int, wordBegin), wordEnd)
                tokens.append(token)

                wordBegin = None
            # Inside a word
            else:
                continue

    return tokens


print(lex('  {   { 123'))
