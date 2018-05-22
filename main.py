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
Token = Tuple[TokenKind, str, int, int]



def get_char(i: int, src: str) -> str:
    if i < len(src):
        return src[i]
    else:
        # Fake space at the end of the string
        return ' '

def get_token_candidates(word: str) -> List[TokenKind]:
    print(('get_token_candidates', word))
    return [
        TokenKind for (TokenKind, matcher) in m if matcher(word)
    ]


# TODO make diagram
def lex(src: str) -> List[Token]:
    state = 0
    index = 0
    line = 1
    lineBase = 0
    partial_token = None
    tokens = []

    max = 0
    while index <= len(src) + 1:
        # TODO make this more explicit when it fails
        if max > 45:
            break
        c = get_char(index, src)
        print(('index', index, 'c', c, 'state', state, 'partial_token', partial_token))
        print(('tokens', tokens))
        if state == 0:
            if c.isspace():
                index += 1
                if c == '\n':
                    line += 1
                    lineBase = index
            else:
                state = 1
                partial_token = (index, line, lineBase)

        elif state == 1:
            (wordBegin, _, _) = partial_token
            # print(('1 partial_token', partial_token))
            word = src[wordBegin:index + 1]
            # print(('1 word', word))
            token_candidates = get_token_candidates(word)
            print(('1: token_candidates', token_candidates))
            is_accepted = len(token_candidates) > 0
            if is_accepted and not c.isspace():
                index += 1
            else:
                # back one character
                index -= 1
                # and move to the token generation state
                state = 2
        elif state == 2:
            # TODO better data structure
            (wordBegin, line, lineBase) = partial_token
            word = src[wordBegin:index + 1]
            # print(('partial_token', partial_token))
            # print(('wordBegin', wordBegin))
            # print(('word', word))
            token_candidates = get_token_candidates(word)
            if len(token_candidates) == 0:
                state = -1
                # TODO better error message
                print('Unrecognized token')
                break
            # print(('prev_token_candidates', prev_token_candidates))
            token_kind = token_candidates[0]
            col = wordBegin - lineBase
            # TODO better data structure
            token = (token_kind, word, line, col)
            print(('new token', token))
            tokens.append(token)

            index += 1
            state = 0
        else:
            state = -1

        max +=1


    error = state == 1
    return (error, tokens)


def printTokens(tokens: List[Token]):
    print("{:^10} {:^10} {:^10} {:^10}".format(*("TokenKind", "lexeme", "line",
                                                 "column")))
    print("------------------------------------------------------------")
    for token in tokens:
        print("{:^10} {:^10} {:^10} {:^10}".format(*token))

    print("++++++++++++++++++++++")
    print(src)
    print("++++++++++++++++++++++")
    for (i, c) in enumerate(src):
        print((i, c))



if __name__ == '__main__':
    src = '  {   { 123\n 123\n   { if'

    (error, tokens) = lex(src)
    printTokens(tokens)
