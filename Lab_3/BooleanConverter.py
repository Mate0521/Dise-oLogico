z = "(not(A and B and C) xnor (A or B)) xnor (not A or not (B and C))"
x = "((A or B) and C xor (A and not B and C)) xor not ((A and B) or (C and B))"


import re
from itertools import product

class BooleanConverter:
    def __init__(self):
        # Mapeo de operadores a sus funciones de conversión
        self.operator_conversions = {
            'xor': self._convert_xor,
            'xnor': self._convert_xnor
        }
        # Precedencia para procesar operadores de mayor anidamiento o más internos
        # Procesar xnor primero (es equivalente a not xor), luego xor
        self.operator_precedence = ['xnor', 'xor'] 

    def _convert_xor(self, op1, op2):
        """Convierte A xor B a (not A and B) or (A and not B)"""
        # Aseguramos paréntesis alrededor de cada operando en la equivalencia
        return f"(not ({op1}) and ({op2})) or (({op1}) and not ({op2}))"

    def _convert_xnor(self, op1, op2):
        """Convierte A xnor B a (A and B) or (not A and not B)"""
        # Aseguramos paréntesis alrededor de cada operando en la equivalencia
        return f"(({op1}) and ({op2})) or (not ({op1}) and not ({op2}))"

    def convert_expression(self, expr):
        """
        Convierte todos los operadores XOR/XNOR en la expresión.
        Procesa de adentro hacia afuera (mayor anidamiento primero) y según la precedencia.
        """
        # Limpiar espacios extra para simplificar el parsing
        expr = re.sub(r'\s+', ' ', expr).strip()

        # Iterar por los operadores según su precedencia
        for op_type in self.operator_precedence:
            # Bucle para procesar todas las ocurrencias del mismo operador
            # La expresión cambiará de longitud, por lo que re-evaluamos la posición
            while True:
                # Buscar el operador de forma case-insensitive
                operator_pattern = r'\b' + re.escape(op_type) + r'\b' # re.escape para seguridad si op_type tuviera caracteres especiales regex
                match = re.search(operator_pattern, expr, re.IGNORECASE)

                if not match:
                    break # No más ocurrencias de este tipo de operador, pasar al siguiente

                op_start_pos = match.start()
                op_end_pos = match.end()

                # Encontrar el inicio del operando izquierdo
                a_start = self._find_operand_start(expr, op_start_pos - 1)
                a_operand = expr[a_start:op_start_pos].strip()

                # Encontrar el fin del operando derecho
                b_end = self._find_operand_end(expr, op_end_pos)
                b_operand = expr[op_end_pos:b_end].strip()

                # Validar que los operandos se encontraron correctamente
                # Si a_operand o b_operand están vacíos, significa que _find_operands falló
                # en encontrar límites válidos para ese operador.
                if not a_operand or not b_operand:
                    # En lugar de insertar '#', vamos a "saltar" esta coincidencia inválida
                    # moviendo el punto de búsqueda más allá de este operador fallido
                    # y continuamos el bucle. Esto puede ser un indicio de una expresión mal formada
                    # o un límite en la lógica de _find_operand_start/_find_operand_end.
                    # Para simplificar, si falla, simplemente pasamos a la siguiente coincidencia
                    # reiniciando la búsqueda después de este operador.
                    # Esto podría dejar operadores sin convertir si están mal formados.
                    # Una solución más avanzada sería lanzar un error o intentar un parsing diferente.
                    # Por ahora, para evitar el bucle infinito y los '#', simplemente intentamos el siguiente.
                    
                    # Para esta iteración, no hacemos ningún reemplazo y buscamos la siguiente coincidencia.
                    # Para que `re.search` encuentre la siguiente, debemos asegurarnos de que la parte actual
                    # no se vuelva a encontrar. Una forma es hacer una pequeña modificación temporal
                    # o asumir que, al fallar, queremos buscar en el resto de la cadena.
                    # Pero como `re.search` siempre busca la primera, si fallamos una vez,
                    # probablemente fallaremos de nuevo en el mismo lugar.
                    # La mejor estrategia es la que ya implementamos: hacer el reemplazo y reiniciar.
                    # Si los operandos están vacíos aquí, es un problema en los _find_operand_X.
                    # De momento, lanzaremos un ValueError si los operandos no son encontrados.
                    raise ValueError(f"No se pudieron encontrar los operandos para '{op_type}' en la posición {op_start_pos}. Expresión parcial: '{expr[max(0, op_start_pos-20):min(len(expr), op_end_pos+20)]}'")

                # Generar el reemplazo usando la función de conversión
                replacement = self.operator_conversions[op_type](a_operand, b_operand)

                # Reconstruir la expresión: antes del operando A + reemplazo + después del operando B
                expr = expr[:a_start] + replacement + expr[b_end:]

                # No necesitamos ajustar `last_pos` porque el `while True`
                # y `re.search` siempre buscarán la primera ocurrencia en la *nueva* `expr`
                # que contiene el reemplazo. Esto es clave para el procesamiento recursivo.

        return expr

    def _find_operand_start(self, expr, end_pos):
        """
        Encuentra el inicio del operando izquierdo buscando hacia atrás desde end_pos.
        Maneja paréntesis balanceados.
        """
        balance = 0
        pos = end_pos
        # Escanear hacia atrás para encontrar el inicio del operando.
        while pos >= 0:
            char = expr[pos]
            if char == ')':
                balance += 1
            elif char == '(':
                balance -= 1
                if balance < 0: # Encontramos un '(' que cierra un bloque exterior, este es el inicio
                    return pos
            # Si el balance es 0 (estamos fuera de paréntesis) y encontramos un operador lógico
            # o un separador que no es parte de una variable/negación.
            elif balance == 0 and char.strip() == '' and pos != end_pos: # Si es un espacio/separador (no el primer char)
                # Nos detuvimos en un espacio. El operando termina antes del espacio.
                return pos + 1
            elif balance == 0 and re.match(r'\b(and|or|not|xor|xnor)\b', expr[pos:end_pos+1], re.IGNORECASE):
                # Si encontramos un operador lógico (que no sea el que estamos procesando)
                # entonces el operando está justo después. Esto es un poco riesgoso si el operador es parte del operando.
                # Es mejor confiar en el balance de paréntesis y espacios.
                pass # No es lo que buscamos como límite principal.
            pos -= 1
        return 0 # Si se llega al principio de la cadena, el operando empieza ahí

    def _find_operand_end(self, expr, start_pos):
        """
        Encuentra el fin del operando derecho buscando hacia adelante desde start_pos.
        Maneja paréntesis balanceados.
        """
        balance = 0
        pos = start_pos
        # Escanear hacia adelante para encontrar el fin del operando.
        while pos < len(expr):
            char = expr[pos]
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0: # Encontramos un ')' que abre un bloque exterior, este es el fin
                    return pos
            # Si el balance es 0 (estamos fuera de paréntesis) y encontramos un operador lógico
            # o un separador que no es parte de una variable.
            elif balance == 0 and char.strip() == '' and pos != start_pos: # Si es un espacio/separador (no el primer char)
                # Nos detuvimos en un espacio. El operando termina antes del espacio.
                return pos
            elif balance == 0 and re.match(r'\b(and|or|not|xor|xnor)\b', expr[start_pos:pos+1], re.IGNORECASE):
                pass # No es lo que buscamos como límite principal.
            pos += 1
        return len(expr) # Si se llega al final de la cadena, el operando termina ahí
    
    def detect_variables(self, expr):
        """Detecta todas las variables mayúsculas en la expresión"""
        # Encuentra letras mayúsculas que no son operadores
        variables = re.findall(r'\b[A-Z]\b', expr)
        # Elimina duplicados y ordena
        return sorted(set(variables))

    def generate_truth_table(self, normalized):
        """Genera la tabla de verdad para la expresión"""
        variables = self.detect_variables(expr)
        
        try:
            # Verificar que la expresión es válida
            compile(normalized, '<string>', 'eval')
        except SyntaxError as e:
            raise ValueError(f"Expresión mal formada: {str(e)}")
        
        table = []
        for values in product([False, True], repeat=len(variables)):
            env = dict(zip(variables, values))
            try:
                result = eval(normalized, {}, env)
                table.append((*values, bool(result)))
            except:
                table.append((*values, None))
        
        return variables, table

    def print_truth_table(self, variables, table):
        """Imprime la tabla de verdad formateada"""
        header = " | ".join(variables + ["Result"])
        print(header)
        print("-" * len(header))
        for row in table:
            print(" | ".join(["1" if x else "0" for x in row]))

# Ejemplo de uso con tus casos de prueba
if __name__ == "__main__":
    converter = BooleanConverter()

    test_cases = [
        z,
        x,

        "A xor (B xnor C)",
        "(A and B) xnor (C xor D)"
    ]

    for expr in test_cases:
        print(f"\nExpresión original: {expr}")
        processed = converter.convert_expression(expr)
        print(f"Expresión procesada: {processed}")
        variables, truth_table = converter.generate_truth_table(processed)
        print("Tabla de verdad:")
        converter.print_truth_table(variables, truth_table)