import sys
from lexer import lexer, LexerError
from parser_transaccion import ParserTransaccion, ParserError

def main():
    if len(sys.argv) != 2:
        print("Uso: python main_transacciones.py archivo.vendi")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tokens = lexer(code)
        parser = ParserTransaccion(tokens)
        transacciones = parser.parse_programa()
        print("Transacciones parseadas:")
        for t in transacciones:
            print(t)
    except (LexerError, ParserError) as e:
        print("❌", e)

if __name__ == "__main__":
    main()
