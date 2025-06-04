from itertools import product
import re

class TruthTableGenerator:
    def detect_variables(self, expr):
        """
        Detecta todas las variables (letras mayúsculas) en una expresión booleana.
        """
        # Encuentra todas las letras mayúsculas (A-Z) como variables, aunque estén juntas
        variables = re.findall(r'[A-Z]', expr)
        return sorted(set(variables))

    def generate_truth_table(self, expr):
        """
        Genera la tabla de verdad para una expresión booleana.
        """
        variables = self.detect_variables(expr)

        # Reemplazar operadores lógicos para que eval los entienda
        expr_eval = expr.replace('and', ' and ').replace('or', ' or ').replace('not', ' not ')

        # Generar todas las combinaciones posibles de True/False
        table = []
        for values in product([False, True], repeat=len(variables)):
            env = dict(zip(variables, values))
            # Reemplazar variables por sus valores en la expresión
            expr_temp = expr_eval
            for var in variables:
                # Reemplaza la variable solo si es una palabra completa
                expr_temp = re.sub(r'\b{}\b'.format(var), str(env[var]), expr_temp)
            try:
                result = eval(expr_temp)
                table.append((*values, bool(result)))
            except Exception as e:
                raise ValueError(f"Error al evaluar expresión: {str(e)}")

        return variables, table

    def print_truth_table(self, variables, table):
        """
        Imprime la tabla de verdad en formato legible.
        """
        header = " | ".join(variables + ["Result"])
        print(header)
        print("-" * len(header))
        for row in table:
            row_str = " | ".join(["1" if val else "0" for val in row])
            print(row_str)