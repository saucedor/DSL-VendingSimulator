# lexer.py
import re
import sys
from tokens import *

class LexerError(Exception):
    pass

# Definición de patrones
tokens = [
    (RESERVADA, r"\b(maquina|producto|precio|stock|pago|transaccion|recarga|retiro|compra|simulacion|efectivo|monedas|billetes|tarjeta|digital|capacidad|etiqueta|cantidad|editar_precio|nuevo_precio)\b"),
    (ESPACIO, r"[ \t\n]+"),
    (ETIQUETA, r"[a-z][0-9]"),
    (IDENTIFICADOR, r"[a-z][a-z0-9_]*"),
    (FLOTANTE, r"[0-9]+\.[0-9]{2}"),
    (ENTERO, r"[0-9]+"),
    (STRING, r"\"[A-Z][A-Za-z0-9_]*\""),
    (BOOLEANO, r"\b(true|false)\b"),
    (SIMBOLO, r"[\{\}\:\;\,]"),
    (COMENTARIO, r"//.*"),
]

# regex maestro
token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in tokens)

def lexer(code):
    tokens_list = []
    pos = 0
    line_num = 1
    col = 1

    for match in re.finditer(token_regex, code):
        if match.start() != pos:
            # Detectar caracteres que no casaron con ningún token
            error_text = code[pos:match.start()]
            line_num = code.count("\n", 0, pos) + 1
            col = pos - code.rfind("\n", 0, pos)
            raise LexerError(
                f"Error léxico en línea {line_num}:{col} - carácter inválido '{error_text}'"
            )

        kind = match.lastgroup
        value = match.group()
        line_num = code.count("\n", 0, match.start()) + 1
        col = match.start() - code.rfind("\n", 0, match.start())

        if kind in ("COMENTARIO", "ESPACIO"):
            pos = match.end()
            continue

        tokens_list.append(Token(kind, value, line_num, col))
        pos = match.end()

    if pos != len(code):
        error_text = code[pos:]
        line_num = code.count("\n", 0, pos) + 1
        col = pos - code.rfind("\n", 0, pos)
        raise LexerError(
            f"Error léxico en línea {line_num}:{col} - carácter inválido '{error_text}'"
        )

    tokens_list.append(Token(EOF, "EOF", line_num, col))
    return tokens_list
