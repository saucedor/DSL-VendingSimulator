# lexer.py
import re
import sys
from tokens import *

# Definición de patrones
tokens = [
    (RESERVADA, r"\b(maquina|producto|precio|stock|pago|transaccion|recarga|retiro|mantenimiento|simulacion)\b"),
    (IDENTIFICADOR, r"[a-z][a-z0-9_]*"),
    (ENTERO, r"[0-9]+"),
    (FLOTANTE, r"[0-9]+\.[0-9]{2}"),
    (STRING, r"\"[A-Z][A-Za-z0-9_]*\""),
    (BOOLEANO, r"\b(true|false)\b"),
    (SIMBOLO, r"[\{\}\:\;\,]"),
    (COMENTARIO, r"//.*"),
]

# regex maestro
token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in tokens)

def lexer(code):
    tokens_list = []
    line_num = 1
    line_start = 0

    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        col = match.start() - line_start + 1

        # calcular número de línea
        line_num = code.count("\n", 0, match.start()) + 1
        line_start = code.rfind("\n", 0, match.start())
        if line_start == -1:
            line_start = 0

        if kind == COMENTARIO:
            continue  # ignorar comentarios
        tokens_list.append(Token(kind, value, line_num, col))

    tokens_list.append(Token(EOF, "EOF", line_num, col))
    return tokens_list
