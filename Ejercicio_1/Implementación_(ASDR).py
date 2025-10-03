class Tokenizer:
    def __init__(self, tokens):
        self.tokens = tokens + ['$']
        self.i = 0
    def lookahead(self):
        return self.tokens[self.i]
    def consume(self, expected=None):
        t = self.tokens[self.i]
        if expected is not None and t != expected:
            raise SyntaxError(f"Se esperaba '{expected}' pero vino '{t}'")
        self.i += 1
        return t
    def pos(self): return self.i
    def set_pos(self,p): self.i = p

class Parser1:
    def __init__(self, tok: Tokenizer):
        self.tok = tok

    def try_rule(self, func):
        saved = self.tok.pos()
        try:
            func()
            return True
        except SyntaxError:
            self.tok.set_pos(saved)
            return False

    def parse_S(self):
        # usamos backtracking seguro:
        if not self.try_rule(self._parse_ABC):
            if not self.try_rule(self._parse_DE):
                raise SyntaxError("S: ninguna alternativa válida")
    def _parse_ABC(self):
        self.parse_A()
        self.parse_B()
        self.parse_C()

    def _parse_DE(self):
        self.parse_D()
        self.parse_E()

    def parse_A(self):
        la = self.tok.lookahead()
        if la == 'dos':
            self.tok.consume('dos')
            self.parse_B()
            self.tok.consume('tres')
        else:
            return

    def parse_B(self):
        while self.tok.lookahead() == 'cuatro':
            self.tok.consume('cuatro')
            self.parse_C()
            self.tok.consume('cinco')

    def parse_C(self):
        la = self.tok.lookahead()
        if la == 'seis':
            self.tok.consume('seis')
            self.parse_A()
            self.parse_B()
        else:
            return

    def parse_D(self):
        la = self.tok.lookahead()
        if la == 'uno':
            self.tok.consume('uno')
            self.parse_A()
            self.parse_E()
        else:
            self.parse_B()

    def parse_E(self):
        self.tok.consume('tres')

# ejemplo de uso:
def test1(tokens):
    tok = Tokenizer(tokens)
    p = Parser1(tok)
    p.parse_S()
    if tok.lookahead() != '$':
        raise SyntaxError("Entrada no consumida completamente (Ej1)")
    print("Ej1: OK — cadena aceptada")
