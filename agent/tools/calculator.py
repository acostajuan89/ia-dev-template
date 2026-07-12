"""
agent/tools/calculator.py — Herramienta de cálculo matemático.

FIX BUG 2: la ejecucion arbitraria de codigo (via la funcion peligrosa
de Python que corre cualquier expresion) fue reemplazada por un parser
AST seguro. Solo se permiten literales numericos y operadores
aritmeticos (+, -, *, /, **, parentesis, negativo unario). Cualquier
otro nodo (imports, llamadas a funcion, nombres, atributos, etc.)
es rechazado por validate() antes de ejecutarse nada.
"""

import ast
import operator
from typing import Any

# Operadores binarios permitidos
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

# Operadores unarios permitidos (ej. -5, +5)
_ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Tipos de nodo permitidos en el árbol (whitelist)
_ALLOWED_NODES = (
    ast.Expression,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
)


def validate(node: ast.AST) -> None:
    """
    Recorre el árbol y lanza ValueError si aparece cualquier nodo
    que no sea aritmética pura (Call, Name, Attribute, Import, etc.).
    """
    if not isinstance(node, _ALLOWED_NODES):
        raise ValueError(f"Expresion no permitida: nodo {type(node).__name__}")

    if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
        raise ValueError(f"Constante no numerica no permitida: {node.value!r}")

    if isinstance(node, ast.BinOp) and type(node.op) not in _ALLOWED_BINOPS:
        raise ValueError(f"Operador no permitido: {type(node.op).__name__}")

    if isinstance(node, ast.UnaryOp) and type(node.op) not in _ALLOWED_UNARYOPS:
        raise ValueError(f"Operador unario no permitido: {type(node.op).__name__}")

    for child in ast.iter_child_nodes(node):
        validate(child)


def safe_eval(node: ast.AST) -> Any:
    """Evalua el árbol ya validado (solo aritmetica pura)."""
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)

    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        return _ALLOWED_UNARYOPS[type(node.op)](operand)

    raise ValueError(f"Expresion no permitida: nodo {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Evalua una expresion matematica de forma segura.

    Args:
        expression: Expresion aritmetica en texto.
                    Soporta: +, -, *, /, //, %, ** y parentesis.

    Returns:
        Resultado como string, o mensaje de error si la expresion es invalida.
    """
    if not isinstance(expression, str):
        return f"ERROR: 'expression' debe ser string, recibio {type(expression).__name__}"

    expression = expression.strip()
    if not expression:
        return "ERROR: expresion vacia"

    try:
        tree = ast.parse(expression, mode="eval")
        validate(tree)
        result: Any = safe_eval(tree)

        if isinstance(result, (int, float)):
            if result == int(result):
                return str(int(result))
            return f"{result:.6g}"
        return f"ERROR: resultado no es numerico: {type(result).__name__}"
    except ZeroDivisionError:
        return "ERROR: division por cero"
    except SyntaxError:
        return "ERROR: expresion invalida"
    except Exception as e:
        return f"ERROR: {e}"