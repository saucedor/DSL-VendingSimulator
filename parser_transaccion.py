import re
from tokens import *

class ParserError(Exception):
    pass

class ParserTransaccion:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.transacciones = []

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

    # --------- Reglas de transacciones ---------
    def parse_programa(self):
        while self.lookahead().tipo != EOF:
            self.parse_transaccion()
        print("✅ Sintaxis de transacciones correcta")
        return self.transacciones

    def parse_transaccion(self):
        self.match(RESERVADA, "transaccion")
        tipo = self.lookahead().valor

        if tipo not in ("compra", "recarga", "retiro", "editar_precio"):
            raise ParserError(
                f"Error en línea {self.lookahead().linea}:{self.lookahead().columna} - tipo de transacción inválido '{tipo}'"
            )

        self.match(RESERVADA, tipo)
        self.match(SIMBOLO, "{")

        if tipo == "compra":
            tx = self.parse_compra()
        elif tipo == "recarga":
            tx = self.parse_recarga()
        elif tipo == "retiro":
            tx = self.parse_retiro()
        elif tipo == "editar_precio":
            tx = self.parse_editar_precio()

        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")

        self.transacciones.append(tx)

    # --------- Transacción: COMPRA ---------
    def parse_compra(self):
        # producto
        self.match(RESERVADA, "producto")
        self.match(SIMBOLO, ":")
        producto = self.match(ETIQUETA).valor
        self.match(SIMBOLO, ";")

        # pago
        self.match(RESERVADA, "pago")
        self.match(SIMBOLO, ":")
        metodo = self.lookahead().valor

        if metodo in ("monedas", "billetes"):
            self.match(RESERVADA, metodo)
            self.match(SIMBOLO, "{")
            efectivo = {}
            denom = int(self.match(ENTERO).valor)
            self.match(SIMBOLO, ":")
            cantidad = int(self.match(ENTERO).valor)
            efectivo[denom] = cantidad

            while self.lookahead().valor == ",":
                self.match(SIMBOLO, ",")
                denom = int(self.match(ENTERO).valor)
                self.match(SIMBOLO, ":")
                cantidad = int(self.match(ENTERO).valor)
                efectivo[denom] = cantidad

            self.match(SIMBOLO, "}")
            self.match(SIMBOLO, ";")
            return {"tipo": "compra", "producto": producto, "pago": {metodo: efectivo}}

        elif metodo in ("tarjeta", "digital"):
            self.match(RESERVADA, metodo)
            self.match(SIMBOLO, ";")
            return {"tipo": "compra", "producto": producto, "pago": metodo}

        else:
            raise ParserError(
                f"Error en línea {self.lookahead().linea}:{self.lookahead().columna} - método de pago inválido '{metodo}'"
            )

    # --------- Transacción: RECARGA ---------
    def parse_recarga(self):
        self.match(RESERVADA, "producto")
        self.match(SIMBOLO, ":")
        producto = self.match(ETIQUETA).valor
        self.match(SIMBOLO, ";")

        self.match(RESERVADA, "cantidad")
        self.match(SIMBOLO, ":")
        cantidad = int(self.match(ENTERO).valor)
        self.match(SIMBOLO, ";")

        return {"tipo": "recarga", "producto": producto, "cantidad": cantidad}

    # --------- Transacción: RETIRO ---------
    def parse_retiro(self):
        self.match(RESERVADA, "efectivo")
        self.match(SIMBOLO, ":")
        self.match(SIMBOLO, "{")

        efectivo = {}
        denom = int(self.match(ENTERO).valor)
        self.match(SIMBOLO, ":")
        cantidad = int(self.match(ENTERO).valor)
        efectivo[denom] = cantidad

        while self.lookahead().valor == ",":
            self.match(SIMBOLO, ",")
            denom = int(self.match(ENTERO).valor)
            self.match(SIMBOLO, ":")
            cantidad = int(self.match(ENTERO).valor)
            efectivo[denom] = cantidad

        self.match(SIMBOLO, "}")
        self.match(SIMBOLO, ";")

        return {"tipo": "retiro", "efectivo": efectivo}
    
    # --------- Transacción: EDITAR PRECIO ---------
    def parse_editar_precio(self):
        self.match(RESERVADA, "producto")
        self.match(SIMBOLO, ":")
        producto = self.match(ETIQUETA).valor
        self.match(SIMBOLO, ";")

        self.match(RESERVADA, "nuevo_precio")
        self.match(SIMBOLO, ":")
        precio_token = self.lookahead()

        if precio_token.tipo == FLOTANTE:
            nuevo_precio = float(self.match(FLOTANTE).valor)
        elif precio_token.tipo == ENTERO:
            nuevo_precio = int(self.match(ENTERO).valor)
        else:
            raise ParserError(
                f"Error en línea {precio_token.linea}:{precio_token.columna} - se esperaba un número para precio"
            )

        self.match(SIMBOLO, ";")

        return {"tipo": "editar_precio", "producto": producto, "nuevo_precio": nuevo_precio}

