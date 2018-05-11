from typing import cast, List, Tuple
import re

m = [
    ('{', re.compile('{$').match),
    ('Number', re.compile('\d+$').match),
]


class LexExcepction(Exception):
    pass


def lex(src: str) -> List[Tuple[str, str, int, int, int]]:
    line = 1
    lineBase = 0
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
                if c == '\n':
                    line += 1
                    lineBase = i
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
                        'Unrecognized Token "' + word + '" in ' + str(line) + str(wordBegin))
                # TODO this needs more work
                column = wordBegin - lineBase + 1
                token = (results[0], word, line, column, wordEnd)
                tokens.append(token)

                wordBegin = None
                
                # TODO avoid duplication
                if c == '\n':
                    line += 1
                    lineBase = i
            # Inside a word
            else:
                continue

    return tokens


src = '  {   { 123\n 123'
print(src)
print(lex(src))

for (i,c) in enumerate(src):
    print((i,c))
