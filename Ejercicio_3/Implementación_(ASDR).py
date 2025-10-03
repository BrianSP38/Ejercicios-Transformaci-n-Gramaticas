class Tokenizer:
    def __init__(self, tokens):
        self.tokens = tokens + ['$']
        self.i = 0
    def lookahead(self):
        return self.tokens[self.i]
    def consume(self, expected=None):
        t = self.tokens[self.i]
        if expected and t != expected:
            raise SyntaxError(f"Se esperaba '{expected}', encontrado '{t}'")
        self.i += 1
        return t

# SELECT sets resumidos (para guiar decisiones)
SELECT_S = {'dos','cuatro','tres','uno','$'}
SELECT_Sp_uno = {'uno'}
SELECT_Sp_eps = {'$'}
SELECT_A_dos = {'dos'}
SELECT_A_eps  = {'cuatro','tres','uno','$'}
SELECT_B_ctres = {'cuatro','tres'}
SELECT_B_eps   = {'cuatro','tres','uno','$'}
SELECT_C_cuatro = {'cuatro'}
SELECT_C_eps    = {'uno','cuatro','tres','$'}

def parse_S(tok: Tokenizer):
    parse_A(tok)
    parse_B(tok)
    parse_C(tok)
    parse_Sp(tok)

def parse_Sp(tok: Tokenizer):
    la = tok.lookahead()
    if la in SELECT_Sp_uno:
        tok.consume('uno')
        parse_Sp(tok)
    elif la in SELECT_Sp_eps:
        return
    else:
        raise SyntaxError(f"En S': token inesperado '{la}'")

def parse_A(tok: Tokenizer):
    la = tok.lookahead()
    if la in SELECT_A_dos:
        tok.consume('dos')
        parse_B(tok)
        parse_C(tok)
    elif la in SELECT_A_eps:
        return
    else:
        raise SyntaxError(f"En A: token inesperado '{la}'")

def parse_B(tok: Tokenizer):
    la = tok.lookahead()
    if la in {'cuatro','tres'}:
        parse_C(tok)
        tok.consume('tres')
    elif la in {'uno','$'}:
        return
    else:
        # hay casos conflictivos (por ejemplo 'cuatro' o 'tres' también aparecen en FOLLOW(B));
        raise SyntaxError(f"En B: token inesperado '{la}'")

def parse_C(tok: Tokenizer):
    la = tok.lookahead()
    if la == 'cuatro':
        tok.consume('cuatro')
        parse_B(tok)
    elif la in {'uno','$','tres'}:
        return
    else:
        raise SyntaxError(f"En C: token inesperado '{la}'")
