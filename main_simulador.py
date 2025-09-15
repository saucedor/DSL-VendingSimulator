import sys
from lexer import lexer, LexerError
from parser_maquina import Parser, ParserError
from parser_transaccion import ParserTransaccion, ParserError as TxError
from simulador import Simulador

def main():
    if len(sys.argv) != 3:
        print("Uso: python main_simulador.py maquina.vendi transacciones.vendi")
        sys.exit(1)

    archivo_maquina, archivo_tx = sys.argv[1], sys.argv[2]

    # Leer y parsear máquina
    with open(archivo_maquina, "r", encoding="utf-8") as f:
        code = f.read()
    tokens = lexer(code)
    maquina = Parser(tokens).parse_programa()

    # Leer y parsear transacciones
    with open(archivo_tx, "r", encoding="utf-8") as f:
        code = f.read()
    tokens_tx = lexer(code)
    transacciones = ParserTransaccion(tokens_tx).parse_programa()

    # Ejecutar simulación
    sim = Simulador(maquina)
    sim.ejecutar_transacciones(transacciones)
    sim.generar_reporte()

if __name__ == "__main__":
    main()
