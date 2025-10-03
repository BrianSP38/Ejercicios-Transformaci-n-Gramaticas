# ASDR con backtracking
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
    def pos(self):
        return self.i
    def set_pos(self, p):
        self.i = p

class Parser2:
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
        if self.try_rule(self._parse_B_uno):
            return
        if self.try_rule(self._parse_dos_C):
            return
        return

    def _parse_B_uno(self):
        self.parse_B()
        self.tok.consume('uno')

    def _parse_dos_C(self):
        self.tok.consume('dos')
        self.parse_C()

    def parse_A(self):
        la = self.tok.lookahead()
        if la == 'cuatro':
            self.tok.consume('cuatro')
            return
        if self.try_rule(self._parse_S_tres_B_C):
            return
        return

    def _parse_S_tres_B_C(self):
        self.parse_S()
        self.tok.consume('tres')
        self.parse_B()
        self.parse_C()

    def parse_B(self):
        if self.try_rule(self._parse_A_cinco_C_seis):
            return
        return

    def _parse_A_cinco_C_seis(self):
        self.parse_A()
        self.tok.consume('cinco')
        self.parse_C()
        self.tok.consume('seis')

    def parse_C(self):
        la = self.tok.lookahead()
        if la == 'siete':
            self.tok.consume('siete')
            self.parse_B()
        else:
            return

# Función de prueba / uso
def test2(tokens):
    tok = Tokenizer(tokens)
    p = Parser2(tok)
    p.parse_S() 
    if tok.lookahead() != '$':
        raise SyntaxError("Entrada no consumida completamente (Ej2)")
    print("Ej2: OK — cadena aceptada")
