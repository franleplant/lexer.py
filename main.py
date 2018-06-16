from typing import cast, List, Tuple, Any
import re

TokenKind = str

# TODO enums?
ACCEPTED = "ACCEPTED"
NOT_ACCEPTED = "NOT_ACCEPTED"
TRAPPED = "TRAPPED"

def a_id(lexeme: str) -> str:
    state = 0
    accepted = [1]
    for c in lexeme:
        if state == 0 and c.isalpha():
            state = 1
        elif state == 1 and c.isalpha():
            state = 1
        else:
            state = -1
            break

    if state == -1:
        return TRAPPED

    if state in accepted:
        return ACCEPTED
    else:
        return NOT_ACCEPTED

def a_num(lexeme: str) -> str:
    state = 0
    accepted = [1]
    for c in lexeme:
        if state == 0 and c.isdigit():
            state = 1
        elif state == 1 and c.isdigit():
            state = 1
        else:
            state = -1
            break

    if state == -1:
        return TRAPPED

    if state in accepted:
        return ACCEPTED
    else:
        return NOT_ACCEPTED

def a_if(lexeme: str) -> str:
    state = 0
    accepted = [2]
    for c in lexeme:
        if state == 0 and c == "i":
            state = 1
        elif state == 1 and c == 'f':
            state = 2
        else:
            state = -1
            break

    if state == -1:
        return TRAPPED

    if state in accepted:
        return ACCEPTED
    else:
        return NOT_ACCEPTED

def a_curly_open(lexeme: str) -> str:
    if lexeme == "{":
        return ACCEPTED
    else:
        return TRAPPED

def a_curly_close(lexeme: str) -> str:
    if lexeme == "}":
        return ACCEPTED
    else:
        return TRAPPED


TOKEN_CONF = [
    ('IF', a_if),
    ('CURLY_OPEN', a_curly_open),
    ('CURLY_CLOSE', a_curly_close),
    ("NUM", a_num),
    ("ID", a_id),
]


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



def lex(src: str) -> List[Token]:
    # TODO do we need this?
    src = src + " "

    tokens: List[Token] = []
    index = 0
    line = 1
    lineBase = 0

    while index < len(src):
        c = src[index]
        if c == '\n':
            line += 1
            lineBase = index

        if c.isspace():
            index += 1
            continue


        start = index
        candidates: List[TokenKind] = []
        next_candidates: List[TokenKind] = []
        lexeme = ""
        next_lexeme = ""
        all_trapped = False

        while not all_trapped:
            all_trapped = True
            lexeme = next_lexeme
            next_lexeme = src[start:index + 1]
            candidates = next_candidates
            next_candidates = []

            for (token_type, afd) in TOKEN_CONF:
                res = afd(next_lexeme)
                if res == ACCEPTED:
                    next_candidates.append(token_type)
                    all_trapped = False
                elif res == NOT_ACCEPTED:
                    all_trapped = False

            # print((lexeme, candidates))
            index += 1


        # rollback one char
        index -= 1

        if len(candidates) == 0:
            print(("tokens", tokens))
            raise Exception("UNKNOWN TOKEN " + lexeme)

        token_type = candidates[0]
        token = Token(token_type, lexeme, line, start - lineBase + 1)
        tokens.append(token)


    return tokens




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
    src = '  {   { 123\n 123\n   {if'

    tokens = lex(src)
    printTokens(tokens)
