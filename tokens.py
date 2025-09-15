# tokens.py

# Tipos de tokens
RESERVADA   = "RESERVADA"
ESPACIO     = "ESPACIO"
ETIQUETA    = "ETIQUETA"
IDENTIFICADOR = "IDENTIFICADOR"
ENTERO      = "ENTERO"
FLOTANTE    = "FLOTANTE"
STRING      = "STRING"
BOOLEANO    = "BOOLEANO"
SIMBOLO     = "SIMBOLO"
COMENTARIO  = "COMENTARIO"
EOF         = "EOF"

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __repr__(self):
        return f"<{self.tipo}, {self.valor}, {self.linea}:{self.columna}>"
