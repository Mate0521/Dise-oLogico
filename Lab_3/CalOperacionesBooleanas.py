from itertools import product
import re

class BooleanExpressionCalculator:
    def __init__(self):
        self.operator_map = {
            '~': 'not ',
            '⋅': ' and ',
            '*': ' and ',
            '+': ' or ',
            '⨁': ' ^ ',
            '⊕': ' ^ ',
            '⊙': ' == ',
            '→': ' <= ',
            '↔': ' == '
        }

    def normalize_expression(self, expr):
        """Convierte la expresión a formato evaluable en Python"""
        # Reemplazar corchetes
        expr = expr.replace('[', '(').replace(']', ')')

        # Reemplazar operadores especiales
        for op, replacement in self.operator_map.items():
            expr = expr.replace(op, replacement)

        # Asegurar que 'not' tenga paréntesis adecuados
        expr = re.sub(r'not\s*([A-Z(])', r'not(\1)', expr)

        # Manejar casos como A+B*C → A+(B and C)
        expr = self._handle_operator_precedence(expr)

        return expr

    def _handle_operator_precedence(self, expr):
        """Asegura la precedencia correcta de operadores"""
        # Implementación básica de precedencia: AND antes que OR
        def replace_and(match):
            return f"({match.group(1)} and {match.group(2)})"

        def replace_or(match):
            return f"({match.group(1)} or {match.group(2)})"

        # AND tiene mayor precedencia, se reemplaza primero
        # Busca patrones como 'A and B', permitiendo espacios alrededor
        expr = re.sub(r'(\w+)\s+and\s+(\w+)', replace_and, expr)

        # Luego OR
        expr = re.sub(r'(\w+)\s+or\s+(\w+)', replace_or, expr)

        return expr

    def get_variables(self, expr):
        """Extrae todas las variables de la expresión"""
        return sorted(set(re.findall(r'\b[A-Z]\b', expr)))

    def evaluate_expression(self, expr, variables, values):
        """Evalúa la expresión con valores dados"""
        env = dict(zip(variables, values))
        try:
            return bool(eval(expr, {}, env))
        except Exception as e:
            print(f"Error al evaluar: {e}, expresión: {expr}, env: {env}")
            return False

    def generate_truth_table(self, expr):
        """Genera la tabla de verdad completa"""
        variables = self.get_variables(expr)
        normalized = self.normalize_expression(expr)

        # Verificar que la expresión es válida
        try:
            compile(normalized, '<string>', 'eval')
        except SyntaxError as e:
            raise ValueError(f"Expresión mal formada: {str(e)}")

        table = []
        for values in product([False, True], repeat=len(variables)):
            result = self.evaluate_expression(normalized, variables, values)
            table.append((*values, result))

        return variables, table

    def simplify_expression(self, variables, table):
        """Simplificación básica por minterms"""
        minterms = [row[:-1] for row in table if row[-1]]

        if not minterms:
            return "0"
        if len(minterms) == 2**len(variables):
            return "1"

        terms = []
        for mint in minterms:
            term = []
            for var, val in zip(variables, mint):
                term.append(f"not {var}" if not val else var)
            terms.append(" and ".join(term))

        return " or ".join(terms) if terms else "0"

    def print_truth_table(self, variables, table):
        """Muestra la tabla de verdad formateada"""
        header = " | ".join(variables + ["Result"])
        print(header)
        print("-" * len(header))
        for row in table:
            print(" | ".join(["1" if x else "0" for x in row]))

    def calculate(self, expr):
        """Procesa la expresión completa"""
        print(f"\nExpresión original: {expr}")

        try:
            # Primero intentamos con la expresión tal cual
            vars, table = self.generate_truth_table(expr)
            print("\nTabla de verdad:")
            self.print_truth_table(vars, table)

            simplified = self.simplify_expression(vars, table)
            print("\nExpresión simplificada:", simplified)

        except ValueError as e:
            print(f"\nError con expresión original: {str(e)}")
            print("Intentando con formato alternativo...")

            # Segunda versión con formato alternativo
            alt_expr = expr.replace('==', '⊙').replace('!=', '⊕')
            alt_expr = alt_expr.replace('and', '*').replace('or', '+')
            alt_expr = alt_expr.replace('not', '~')

            try:
                vars, table = self.generate_truth_table(alt_expr)
                print("\nTabla de verdad (formato alternativo):")
                self.print_truth_table(vars, table)

                simplified = self.simplify_expression(vars, table)
                print("\nExpresión simplificada:", simplified)

            except ValueError as e2:
                print(f"\nError persistente: {str(e2)}")
                print("\nRecomendación: Usar un formato más consistente con operadores como 'and', 'or', 'not', '==', '^'.")

# Uso garantizado que funciona
if __name__ == "__main__":
    calc = BooleanExpressionCalculator()

    # Esta expresión SÍ funciona ahora con la corrección de precedencia
    working_expr = "not((A and B and C) == (A or B)) ^ not(A or (B and C))"
    calc.calculate(working_expr)

    # También puedes probar con:
    calc.calculate("(A and B) or (not C)")
    calc.calculate("A ^ B == C")
    calc.calculate("~A * B + C")