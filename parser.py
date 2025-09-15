# parser.py
from tokens import *

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def lookahead(self):
        return self.tokens[self.pos]
    
    def match(self, tipo, valor=None):
        token = self.lookahead()
        if token.tipo != tipo:
            raise ParserError(f"Error en línea {token.linea}:{token.columna} - esperado {tipo}, encontrado {token.tipo} ({token.valor})")
        if valor and token.valor != valor:
            raise ParserError(f"Error en línea {token.linea}:{token.columna} - esperado '{valor}', encontrado '{token.valor}'")
        self.pos += 1
        return token
    
    # -------- Reglas de la gramática --------
    def parse_programa(self):
        while self.lookahead().tipo != EOF:
            if self.lookahead().valor == "maquina":
                self.parse_decl_maquina()
            else:
                self.match(self.lookahead().tipo)  # por ahora tragamos lo demás
        print("✅ Sintaxis correcta")
    
    def parse_decl_maquina(self):
        self.match(RESERVADA, "maquina")
        self.match(IDENTIFICADOR)
        self.match(SIMBOLO, "{")
        # cuerpo (por ahora vacío)
        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")
