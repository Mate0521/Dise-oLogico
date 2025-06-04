from itertools import product
import re

class TruthTableGenerator:
    def detect_variables(self, expr):
        """
        Detecta todas las variables (letras mayúsculas) en una expresión booleana.
        
        Args:
            expr (str): Expresión booleana ya procesada (solo con not, and, or)
            
        Returns:
            list: Lista ordenada de variables únicas
        """
        # Encuentra todas las letras mayúsculas que no son parte de operadores
        variables = re.findall(r'\b[A-Z]\b', expr)
        return sorted(set(variables))

    def generate_truth_table(self, expr):
        """
        Genera la tabla de verdad para una expresión booleana.
        
        Args:
            expr (str): Expresión booleana ya procesada (solo con not, and, or)
            
        Returns:
            tuple: (variables, table) donde:
                - variables: lista de variables
                - table: lista de tuplas con (valores, resultado)
        """
        variables = self.detect_variables(expr)
        
        # Verificar que la expresión es válida
        try:
            compiled_expr = compile(expr, '<string>', 'eval')
        except SyntaxError as e:
            raise ValueError(f"Expresión mal formada: {str(e)}")

        table = []
        # Generar todas las combinaciones posibles de True/False
        for values in product([False, True], repeat=len(variables)):
            # Crear entorno de evaluación {variable: valor}
            env = dict(zip(variables, values))
            try:
                result = eval(compiled_expr, {}, env)
                table.append((*values, bool(result)))
            except Exception as e:
                raise ValueError(f"Error al evaluar expresión: {str(e)}")
        
        return variables, table

    def print_truth_table(self, variables, table):
        """
        Imprime la tabla de verdad en formato legible.
        
        Args:
            variables (list): Lista de variables
            table (list): Tabla de verdad generada por generate_truth_table()
        """
        # Encabezado
        header = " | ".join(variables + ["Result"])
        print(header)
        print("-" * len(header))
        
        # Filas
        for row in table:
            # Convertir True/False a 1/0 para mejor visualización
            row_str = " | ".join(["1" if val else "0" for val in row])
            print(row_str)