from parser_maquina import Parser, ParserError
from parser_transaccion import ParserTransaccion, ParserError as TxError
from lexer import lexer, LexerError

class Simulador:
    def __init__(self, maquina):
        self.maquina = maquina  # objeto dict generado por parser_maquina
        self.ventas = []
        self.recargas = []
        self.retiros = []

    def ejecutar_transacciones(self, transacciones):
        for tx in transacciones:
            tipo = tx["tipo"]
            if tipo == "compra":
                self.procesar_compra(tx)
            elif tipo == "recarga":
                self.procesar_recarga(tx)
            elif tipo == "retiro":
                self.procesar_retiro(tx)
            elif tipo == "editar_precio":
                self.procesar_editar_precio(tx)

    # ---------- Lógica de cada transacción ----------
    def procesar_compra(self, tx):
        producto = tx["producto"]
        if producto not in self.maquina["productos"]:
            print(f"❌ Producto {producto} no existe")
            return

        item = self.maquina["productos"][producto]
        if item["stock"] <= 0:
            print(f"❌ Producto {producto} agotado")
            return

        # reducir stock
        item["stock"] -= 1
        # sumar venta
        self.ventas.append({"producto": producto, "precio": item["precio"], "pago": tx["pago"]})
        print(f"✅ Compra realizada: {producto} por {item['precio']}")

    def procesar_recarga(self, tx):
        producto = tx["producto"]
        cantidad = tx["cantidad"]
        if producto not in self.maquina["productos"]:
            print(f"❌ No existe producto {producto}")
            return

        self.maquina["productos"][producto]["stock"] += cantidad
        self.recargas.append(tx)
        print(f"✅ Recarga: {cantidad} unidades a {producto}")

    def procesar_retiro(self, tx):
        # Para simplificar: solo registramos la acción
        self.retiros.append(tx)
        print(f"✅ Retiro de efectivo: {tx['efectivo']}")

    def procesar_editar_precio(self, tx):
        producto = tx["producto"]
        nuevo_precio = tx["nuevo_precio"]

        if producto not in self.maquina["productos"]:
            print(f"❌ No existe producto {producto}")
            return

        self.maquina["productos"][producto]["precio"] = nuevo_precio
        print(f"✅ Precio de {producto} actualizado a {nuevo_precio}")

    # ---------- Reporte final ----------
    def generar_reporte(self, archivo="reporte_final.txt"):
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("=== REPORTE FINAL DE SIMULACION ===\n")
            f.write(f"Máquina: {self.maquina['nombre']}\n\n")

            f.write("Productos:\n")
            for etiqueta, prod in self.maquina["productos"].items():
                f.write(f"  {etiqueta}: {prod['nombre']} - precio: {prod['precio']} - stock: {prod['stock']}\n")

            f.write("\nVentas realizadas:\n")
            for v in self.ventas:
                f.write(f"  {v['producto']} pagado con {v['pago']} por {v['precio']}\n")

            f.write("\nRecargas:\n")
            for r in self.recargas:
                f.write(f"  {r['producto']} +{r['cantidad']}\n")

            f.write("\nRetiros:\n")
            for rt in self.retiros:
                f.write(f"  {rt['efectivo']}\n")

        print(f"📂 Reporte generado en {archivo}")
