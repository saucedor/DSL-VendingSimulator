from tokens import *
import re

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.productos = {}  # etiquetas vistas (para validar duplicados)
    
    def lookahead(self):
        return self.tokens[self.pos]
    
    def match(self, tipo, valor=None):
        token = self.lookahead()
        if token.tipo != tipo:
            raise ParserError(
                f"Error en línea {token.linea}:{token.columna} - esperado {tipo}, encontrado {token.tipo} ({token.valor})"
            )
        if valor and token.valor != valor:
            raise ParserError(
                f"Error en línea {token.linea}:{token.columna} - esperado '{valor}', encontrado '{token.valor}'"
            )
        self.pos += 1
        return token
    
    # -------- Reglas de la gramática --------
    def parse_programa(self):
        maquina = None
        while self.lookahead().tipo != EOF:
            token = self.lookahead()
            if token.valor == "maquina":
                maquina = self.parse_decl_maquina()
            else:
                raise ParserError(
                    f"Error en línea {token.linea}:{token.columna} - declaración inesperada '{token.valor}'"
                )
        print("✅ Sintaxis correcta")
        return maquina
    
    def parse_decl_maquina(self):
        self.match(RESERVADA, "maquina")
        nombre = self.match(IDENTIFICADOR).valor
        self.match(SIMBOLO, "{")

        capacidad_max = None
        productos = {}

        while self.lookahead().valor in ("producto", "capacidad", "pago", "efectivo"):
            if self.lookahead().valor == "capacidad":
                capacidad_max = self.parse_capacidad()
            elif self.lookahead().valor == "producto":
                prod = self.parse_decl_producto()
                productos[prod["etiqueta"]] = prod
            elif self.lookahead().valor == "pago":
                self.parse_metodos_pago()
            elif self.lookahead().valor == "efectivo":
                self.parse_inventario_efectivo()

        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")

        if capacidad_max is not None and len(productos) > capacidad_max:
            raise ParserError(
                f"Error: se declararon {len(productos)} productos pero la capacidad máxima es {capacidad_max}"
            )

        return {
            "nombre": nombre,
            "capacidad": capacidad_max,
            "productos": productos
        }

    def parse_capacidad(self):
        self.match(RESERVADA, "capacidad")
        self.match(SIMBOLO, ":")
        valor = int(self.match(ENTERO).valor)
        self.match(SIMBOLO, ";")
        return valor

    def parse_decl_producto(self):
        self.match(RESERVADA, "producto")
        nombre_producto = self.match(IDENTIFICADOR).valor

        if not re.fullmatch(r"[a-z][a-z0-9_]*", nombre_producto):
            raise ParserError(
                f"Error: nombre de producto inválido '{nombre_producto}' "
                f"(solo minúsculas, números y '_')"
            )

        self.match(SIMBOLO, "{")
        etiqueta = self.parse_decl_etiqueta()
        precio, stock = self.parse_precio_y_stock()
        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")

        if etiqueta in self.productos:
            raise ParserError(
                f"Error: etiqueta '{etiqueta}' ya fue usada para otro producto"
            )
        self.productos[etiqueta] = nombre_producto

        if stock > 10:
            raise ParserError(
                f"Error: producto '{nombre_producto}' con etiqueta '{etiqueta}' excede stock máximo (10)"
            )

        return {
            "nombre": nombre_producto,
            "etiqueta": etiqueta,
            "precio": precio,
            "stock": stock
        }

    def parse_decl_etiqueta(self):
        self.match(RESERVADA, "etiqueta")
        self.match(SIMBOLO, ":")
        etiqueta_valor = self.match(ETIQUETA).valor
        self.match(SIMBOLO, ";")
        return etiqueta_valor

    def parse_precio_y_stock(self):
        # precio
        self.match(RESERVADA, "precio")
        self.match(SIMBOLO, ":")
        if self.lookahead().tipo == FLOTANTE:
            precio = float(self.match(FLOTANTE).valor)
        elif self.lookahead().tipo == ENTERO:
            precio = int(self.match(ENTERO).valor)
        else:
            t = self.lookahead()
            raise ParserError(
                f"Error en línea {t.linea}:{t.columna} - esperado número en precio, encontrado {t.tipo} ({t.valor})"
            )
        self.match(SIMBOLO, ";")

        # stock
        self.match(RESERVADA, "stock")
        self.match(SIMBOLO, ":")
        stock_valor = int(self.match(ENTERO).valor)
        self.match(SIMBOLO, ";")

        return precio, stock_valor

    def parse_metodos_pago(self):
        self.match(RESERVADA, "pago")
        self.match(SIMBOLO, ":")
        self.parse_metodo_pago()
        while self.lookahead().tipo == SIMBOLO and self.lookahead().valor == ",":
            self.match(SIMBOLO, ",")
            self.parse_metodo_pago()
        self.match(SIMBOLO, ";")

    def parse_metodo_pago(self):
        token = self.lookahead()
        if token.valor in ("monedas", "billetes", "tarjeta", "digital"):
            self.match(RESERVADA, token.valor)
        else:
            raise ParserError(
                f"Error en línea {token.linea}:{token.columna} - método de pago inválido '{token.valor}'"
            )

    def parse_inventario_efectivo(self):
        self.match(RESERVADA, "efectivo")
        self.match(SIMBOLO, ":")
        self.match(SIMBOLO, "{")

        # par denom: cantidad
        self.match(ENTERO)
        self.match(SIMBOLO, ":")
        self.match(ENTERO)

        while self.lookahead().tipo == SIMBOLO and self.lookahead().valor == ",":
            self.match(SIMBOLO, ",")
            self.match(ENTERO)
            self.match(SIMBOLO, ":")
            self.match(ENTERO)

        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")
