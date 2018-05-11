from typing import cast, List, Tuple
import re

m = [
    ('{', re.compile('{$').match),
    ('Number', re.compile('\d+$').match),
]


class LexExcepction(Exception):
    pass


def lex(src: str) -> List[Tuple[str, str, int, int]]:
    line = 1
    lineBase = 0
    tokens = []
    wordBegin = 0
    insideWord = False
    for i in range(0, len(src) + 1):
        c = None
        if i < len(src):
            c = src[i]
        else:
            # Fake space at the end of the string
            c = ' '

        if not insideWord and not c.isspace():
            wordBegin = i
            insideWord = True
        if insideWord and c.isspace():
            wordEnd = i
            word = src[wordBegin:wordEnd]
            results = [
                TokenKind for (TokenKind, matcher) in m if matcher(word)
            ]
            if len(results) == 0:
                raise LexExcepction('Unrecognized Token "' + word + '" in ' +
                                    str(line) + str(wordBegin))
            column = wordBegin - lineBase + 1
            token = (results[0], word, line, column)
            tokens.append(token)

            insideWord = False

        if c == '\n':
            line += 1
            lineBase = i + 1

    return tokens


src = '  {   { 123\n 123\n   {'

print("{:^10} {:^10} {:^10} {:^10}".format(*("TokenKind", "lexeme", "line",
                                             "column")))
print("------------------------------------------------------------")
for token in lex(src):
    print("{:^10} {:^10} {:^10} {:^10}".format(*token))

print("++++++++++++++++++++++")
print(src)
print("++++++++++++++++++++++")
for (i, c) in enumerate(src):
    print((i, c))
