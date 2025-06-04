z = "(((not (A and B and C) and (A or B)) or (not (not (A and B and C)) and not (A or B))) and (not A or not (B and C))) or (not ((not (A and B and C) and (A or B)) or (not (not (A and B and C)) and not (A or B))) and not (not A or not (B and C)))"

x = "((((A or B) and C and not (A and not B and C)) or (not ((A or B) and C) and (A and not B and C))) and not (not ((A and B) or (C and B)))) or (not (((A or B) and C and not (A and not B and C)) or (not ((A or B) and C) and (A and not B and C))) and not (not ((A and B) or (C and B))))"

from logica.BooleanConverter import BooleanConverter
from logica.TruthTableGenerator import TruthTableGenerator
from logica.BooleanSimplifier import BooleanSimplifier  


if __name__ == "__main__": 
    converter = BooleanConverter()
    generator = TruthTableGenerator()
    simplifier = BooleanSimplifier()
    
    test_cases = [
        z,
        x,
        "A xor (B xnor C)",
        "(A and B) xnor (C xor D)",
        "A or B",
    ]
    
    for expr in test_cases:
        print(f"\n{'='*50}\nExpresión original: {expr}")
        
        try:
            # Convertir expresión
            processed = converter.convert_expression(expr)
            print(f"Expresión procesada: {processed}")
            
            # Generar tabla de verdad
            variables, truth_table = generator.generate_truth_table(expr)
            
            # Mostrar resultados
            print("\nVariables detectadas:", variables)
            print("\nTabla de verdad:")
            generator.print_truth_table(variables, truth_table)

            # Simplificar expresión
            simplified = simplifier.simplify(expr)
            print(f"Expresión simplificada: {simplified}")
            
        except ValueError as e:
            print(f"\nError: {str(e)}")