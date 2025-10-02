tokens = [...]     
pos = 0
def lookahead():
    return tokens[pos] if pos < len(tokens) else '$'
def match(tok):
    global pos
    if lookahead() == tok:
        pos += 1
    else:
        raise SyntaxError(f"Expected {tok} but found {lookahead()}")


def S():
    la = lookahead()
    # Nota: conflicto en 'cuatro' (ambas alternativas). Aquí mostramos la estructura:
    if la in {'dos', 'seis', '$'}:
        A()
        B()
        C()
    elif la in {'uno', 'tres'}:
        D()
        E()
    elif la == 'cuatro':
        # conflicto: tanto S->A B C como S->D E son posibles cuando la == 'cuatro'
        # Necesitamos reescribir la gramática o usar backtracking.
        save = pos
        try:
            A(); B(); C()
            return
        except SyntaxError:
            pos = save
            D(); E()
    else:
        raise SyntaxError("error en S, token inesperado "+la)

def A():
    la = lookahead()
    if la == 'dos':
        match('dos')
        B()
        match('tres')
    elif la in {'$', 'cinco','cuatro','seis','tres'}:
        return
    else:
        raise SyntaxError("error en A")

def B():
    B2()

def B2():
    la = lookahead()
    if la == 'cuatro':
        match('cuatro')
        C()
        match('cinco')
        B2()
    elif la in {'$','cinco','seis','tres'}:
        return
    else:
        raise SyntaxError("error en B2")

def C():
    la = lookahead()
    if la == 'seis':
        match('seis')
        A()
        B()
    elif la in {'$','cinco'}:
        return
    else:
        raise SyntaxError("error en C")

def D():
    la = lookahead()
    if la == 'uno':
        match('uno')
        A()
        E()
    elif la == 'cuatro' or la in {'$','cinco','seis','tres'}:
        B()
    else:
        raise SyntaxError("error en D")

def E():
    match('tres')
