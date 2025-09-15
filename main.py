# main.py
import sys
from lexer import lexer
from parser import Parser, ParserError

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py archivo.vendi")
        sys.exit(1)
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()
    
    try:
        tokens = lexer(code)
        parser = Parser(tokens)
        parser.parse_programa()
    except ParserError as e:
        print("❌", e)
    except Exception as e:
        print("❌ Error inesperado:", e)

if __name__ == "__main__":
    main()
