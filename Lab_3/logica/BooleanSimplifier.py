import re

# Clase para simplificar expresiones booleanas usando solo condicionales
class BooleanSimplifier:
    def simplify(self, expr):
        """
        Simplifica una expresión booleana representada como string,
        usando reglas básicas y condicionales (sin librerías externas).
        Solo soporta and, or, not, paréntesis y variables de una letra.
        """
        expr = expr.replace(' ', '')

        # Simplificación iterativa
        prev = None
        while prev != expr:
            prev = expr

            # Doble negación
            expr = expr.replace('notnot', '')

            # Identidad y anulación
            expr = expr.replace('andTrue', '')
            expr = expr.replace('Trueand', '')
            expr = expr.replace('orFalse', '')
            expr = expr.replace('Falseor', '')

            # Dominación
            expr = expr.replace('andFalse', 'False')
            expr = expr.replace('Falseand', 'False')
            expr = expr.replace('orTrue', 'True')
            expr = expr.replace('Trueor', 'True')

            # Idempotencia y negación para variables de una letra
            for v in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                expr = expr.replace(f'{v}and{v}', v)
                expr = expr.replace(f'{v}or{v}', v)
                expr = expr.replace(f'{v}andnot{v}', 'False')
                expr = expr.replace(f'not{v}and{v}', 'False')
                expr = expr.replace(f'{v}ornot{v}', 'True')
                expr = expr.replace(f'not{v}or{v}', 'True')

                # Absorción
                expr = expr.replace(f'{v}or({v}and', f'{v}or(')  # A or (A and X) -> A or (X)
                expr = expr.replace(f'{v}and({v}or', f'{v}and(')  # A and (A or X) -> A and (X)

            # Factorización para patrones con paréntesis simples: (A and X) or (A and Y) -> A and (X or Y)
            for v in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                for w in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    for u in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                        # Busca patrones tipo (AandB)or(AandC)
                        pattern = f'({v}and{w})or({v}and{u})'
                        if pattern in expr:
                            expr = expr.replace(pattern, f'{v}and({w}or{u})')

            # Ley de De Morgan para paréntesis simples: not((AandB)), not((AorB))
            i = 0
            while i < len(expr):
                if expr[i:i+4] == 'not(':
                    # Buscar el cierre del paréntesis correspondiente
                    count = 1
                    j = i+4
                    while j < len(expr) and count > 0:
                        if expr[j] == '(':
                            count += 1
                        elif expr[j] == ')':
                            count -= 1
                        j += 1
                    if count == 0:
                        inside = expr[i+4:j-1]
                        # Solo aplica si es una conjunción o disyunción simple
                        if 'and' in inside and 'or' not in inside:
                            partes = inside.split('and')
                            if len(partes) == 2:
                                nueva = f'(not{partes[0]}ornot{partes[1]})'
                                expr = expr[:i] + nueva + expr[j:]
                                continue
                        if 'or' in inside and 'and' not in inside:
                            partes = inside.split('or')
                            if len(partes) == 2:
                                nueva = f'(not{partes[0]}andnot{partes[1]})'
                                expr = expr[:i] + nueva + expr[j:]
                                continue
                i += 1

        return expr

# Ejemplo de uso
if __name__ == "__main__":
    simplifier = BooleanSimplifier()
    expresion = "((A and B) or (A and C)) and not(A and notA)"
    print("Original:", expresion)
    print("Simplificada:", simplifier.simplify(expresion))