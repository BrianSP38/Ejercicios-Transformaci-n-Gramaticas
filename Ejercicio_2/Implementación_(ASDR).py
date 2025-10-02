
tokens = [...]
pos = 0
def lookahead(): ...
def match(tok): ...

# Funciones para Ejercicio 2

def S():
    la = lookahead()
    if la in {'dos'}:
        match('dos')
        C()
    elif la in {'uno','cuatro','tres','cinco'}:
        # Nota: esto incluye 'dos' también en teoría por derivaciones de B,
        # pero aquí separamos 'dos' explicitamente arriba para evitar ambiguedad parcial.
        B()
        match('uno')
    elif la in {'$', 'tres'}:
        # S -> epsilon (si la está en FOLLOW(S)) ; cuidado: 'tres' también está en predicción de S->B uno
        # por ello hay conflicto en 'tres' (requiere reescritura o backtracking)
        return
    else:
        raise SyntaxError("error en S")

def A():
    la = lookahead()
    if la in {'uno','dos','cuatro','tres','cinco'}:
        if la == 'cuatro':
            match('cuatro')
            return
        else:
            S()
            match('tres')
            B()
            C()
    elif la == 'cinco':
        return
    else:
        raise SyntaxError("error en A")

def B():
    la = lookahead()
    if la in {'uno','dos','cuatro','tres','cinco'}:
        A()
        match('cinco')
        C()
        match('seis')
    elif la in {'$','cinco','seis','siete','tres','uno'}:
        return
    else:
        raise SyntaxError("error en B")

def C():
    la = lookahead()
    if la == 'siete':
        match('siete')
        B()
    elif la in {'$','cinco','seis','tres'}:
        return
    else:
        raise SyntaxError("error en C")
