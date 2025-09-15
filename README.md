## Video de YT con demostración/explicación: https://youtu.be/3l6wIr63v9k

# Proyecto VendiXpress – Simulación de Máquinas Expendedoras
Para este proyecto de Evidencia 1 en la clase de implementación de métodos computacionales, se desarrolló un un sistema que tiene como objetivo diseñar un lenguaje específico de dominio (DSL) en español para describir y simular el comportamiento de una máquina expendedora. 

El sistema desarrollado permite:

- **Definir máquinas expendedoras** mediante archivos `.vendi`, indicando nombre, capacidad máxima de productos, métodos de pago aceptados, inventario de productos y efectivo inicial.
- **Validar la sintaxis y gramática** de estas definiciones usando un analizador léxico (con expresiones regulares) y un parser de descenso recursivo.
- **Procesar transacciones** de clientes y administradores mediante un archivo independiente de transacciones:
  - Compras de productos con diferentes métodos de pago.
  - Recarga de inventario.
  - Retiros de efectivo.
  - Edición de precios de productos.
- **Ejecutar una simulación completa** donde las transacciones afectan el estado de la máquina y se genera un reporte final en formato `.txt`.

---

## Archivos principales

- `lexer.py` → Analizador léxico.  
- `parser_maquina.py` → Parser para declaraciones de máquinas.  
- `parser_transaccion.py` → Parser para transacciones.  
- `simulador.py` → Motor de simulación que integra máquina y transacciones.  
- `main_simulador.py` → Script principal para correr la simulación.  
- `examples/ejemplo_maquina.vendi` → Ejemplo de declaración de máquina.  
- `examples/ejemplo_transacciones.vendi` → Ejemplo de transacciones.  

---

## Comandos para correr el programa

### 1. Correr simulación 
```bash
python main_simulador.py examples/ejemplo_demostracion_maquina.vendi examples/ejemplo_demostracion_transacciones.vendi
```
### 2. válidar sintaxis de la máquina
```bash
python main_maquina.py examples/ejemplo_demostracion_maquina.vendi   
```
### 3. válidar sintaxis de la máquina
```bash
python main_transacciones.py examples/ejemplo_demostracion_transacciones.vendi
```

