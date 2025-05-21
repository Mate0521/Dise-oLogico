import itertools
from sympy import symbols, simplify_logic, Equivalent
from sympy.parsing.sympy_parser import parse_expr

# Traducción a operadores de Python/sympy
def traducir_expresion(expr):
    traducciones = {
        '¬': '~',
        '⋅': '&',
        '+': '|',
        '⊕': '^',
        '⊙': '==',
        '[': '(',
        ']': ')',
    }
    for simbolo, reemplazo in traducciones.items():
        expr = expr.replace(simbolo, reemplazo)
    # Agrupar todo lo que está después de un ~ para evitar errores
    expr = expr.replace('~(', '~((')  # abre dos veces
    expr = expr.replace(')^', '))^')  # cierra dos veces antes del XOR
    return expr



# Obtener variables únicas
def obtener_variables(expresion):
    return sorted(set(filter(str.isalpha, expresion)))

# Crear tabla de verdad
def generar_tabla_verdad(expr_str, variables):
    simbolos = symbols(variables)
    contexto_simbolos = dict(zip(variables, simbolos))
    expr = parse_expr(expr_str, evaluate=False, local_dict=contexto_simbolos)
    tabla = []
    for valores in itertools.product([0, 1], repeat=len(variables)):
        contexto_valores = dict(zip(simbolos, valores))
        resultado = int(expr.subs(contexto_valores))
        tabla.append((*valores, resultado))
    return tabla

# Mostrar tabla
def imprimir_tabla(tabla, variables, nombre="Tabla de Verdad"):
    print(f"\n🧮 {nombre}")
    print(' | '.join(variables + ['Z']))
    print('-' * (4 * len(variables) + 3))
    for fila in tabla:
        print(' | '.join(str(v) for v in fila))

# Simplificar la expresión
def simplificar(expr_str, variables):
    simbolos = symbols(variables)
    contexto_simbolos = dict(zip(variables, simbolos))
    expr = parse_expr(expr_str, evaluate=False, local_dict=contexto_simbolos)
    simplificada = simplify_logic(expr, form='dnf')  # Puedes cambiar a 'cnf' si prefieres
    return simplificada

# -------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------
expresion_original = "¬[(A⋅B⋅C)⊙(A+B)]⊕¬(A+B⋅C)"


# Paso 1: traducir
expr_traducida = traducir_expresion(expresion_original)
print(f"\n📥 Expresión original: {expresion_original}")
print(f"📘 Expresión traducida: {expr_traducida}")

# Paso 2: obtener variables
vars_en_expr = obtener_variables(expr_traducida)
print(f"📌 Variables: {vars_en_expr}")

# Paso 3: tabla de verdad original
tabla_original = generar_tabla_verdad(expr_traducida, vars_en_expr)
imprimir_tabla(tabla_original, vars_en_expr, "Tabla de Verdad Original")

# Paso 4: simplificación
expr_simplificada = simplificar(expr_traducida, ''.join(vars_en_expr))
print(f"\n🧠 Expresión simplificada: {expr_simplificada}")

# Paso 5: tabla de verdad simplificada
tabla_simplificada = generar_tabla_verdad(str(expr_simplificada), vars_en_expr)
imprimir_tabla(tabla_simplificada, vars_en_expr, "Tabla de Verdad Simplificada")
