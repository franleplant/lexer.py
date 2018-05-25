from typing import cast, List, Tuple, Any
import re


def if_automata(input: str) -> bool:
    state = 0
    for c in input:
        if state == 0 and c == "i":
            state = 1
            continue
        elif state == 1 and c == 'f':
            state = 2
            continue
        else:
            state = -1
            break

    # is it acepted?
    return state == 2


m: List[Any] = [
    ('{', re.compile('^{$').match),
    ('If', if_automata),
    ('Number', re.compile('^\d+$').match),
    ('Id', re.compile('^[a-zA-Z]+$').match)
]


class LexExcepction(Exception):
    pass

TokenKind = str
class Token:
    def __init__(self, token_kind: TokenKind, lexeme: str, line: int, col: int) -> None:
        self.kind = token_kind
        self.lexeme = lexeme
        self.line = line
        self.col = col

    def __eq__(self, other):
        """Overrides the default implementation"""
        if type(other) is tuple:
            return self.kind == other[0] and self.lexeme == other[1] and self.line == other[2] and self.col == other[3]

        return NotImplemented


    def __repr__(self):
        return "TOKEN: {} {} {} {}".format(self.kind, self.lexeme, self.line, self.col)



class PotentialToken:
    def __init__(self, startIndex: int, line: int, lineBase: int) -> None:
        self.start = startIndex
        self.line = line
        self.lineBase = lineBase

    def col(self) -> int:
        return self.start - self.lineBase + 1


    def to_token(self, token_kind: TokenKind, word: str) -> Token:
        return Token(token_kind, word, self.line, self.col())




def get_char(i: int, src: str) -> str:
    if i < len(src):
        return src[i]
    else:
        # Fake space at the end of the string
        return ' '

def get_token_candidates(word: str) -> List[TokenKind]:
    return [
        TokenKind for (TokenKind, matcher) in m if matcher(word)
    ]


MAX_ITERATIONS = 200
# TODO make diagram
# TODO make number convertions?
def lex(src: str) -> Tuple[bool, List[Token]]:
    state = 0
    index = 0
    line = 1
    lineBase = 0
    potential_token = None
    tokens = []

    iter_count = 0
    while index <= len(src) + 1:
        if iter_count > MAX_ITERATIONS:
            raise Exception('ERROR MAX_ITERATIONS')

        c = get_char(index, src)

        # Initial White space skip
        if state == 0:
            if c.isspace():
                index += 1
                if c == '\n':
                    line += 1
                    lineBase = index
            else:
                state = 1
                potential_token = PotentialToken(index, line, lineBase)

        # While being at least one potential accepted token consume characters
        elif state == 1:
            if potential_token is None:
                raise Exception('1: something really bad happened')
            word = src[potential_token.start:index + 1]
            token_candidates = get_token_candidates(word)
            is_accepted = len(token_candidates) > 0
            if is_accepted and not c.isspace():
                index += 1
            else:
                # back one character
                index -= 1
                # and move to the token generation state
                state = 2

        # Max length token detected, create one and restart the process
        elif state == 2:
            if potential_token is None:
                raise Exception('2: something really bad happened')
            word = src[potential_token.start:index + 1]
            token_candidates = get_token_candidates(word)
            if len(token_candidates) == 0:
                state = -1
                # TODO better error message
                print('Unrecognized token')
                break

            token_kind = token_candidates[0]
            token = potential_token.to_token(token_kind, word)
            # print(('new token', token))
            tokens.append(token)

            index += 1
            state = 0
        else:
            state = -1

        iter_count +=1


    error = state == 1
    return (error, tokens)


def printTokens(tokens: List[Token]):
    print("{:^10} {:^10} {:^10} {:^10}".format(*("TokenKind", "lexeme", "line",
                                                 "column")))
    print("------------------------------------------------------------")
    for token in tokens:
        print("{:^10} {:^10} {:^10} {:^10}".format(token.kind, token.lexeme, token.line, token.col))

    print("++++++++++++++++++++++")
    print(src)
    print("++++++++++++++++++++++")
    for (i, c) in enumerate(src):
        print((i, c))



if __name__ == '__main__':
    src = '  {   { 123\n 123\n   { if'

    (error, tokens) = lex(src)
    printTokens(tokens)
