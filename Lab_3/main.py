z = "(not(A and B and C) xnor (A or B)) xnor (not A or not (B and C))"
x = "((A or B) and C xor (A and not B and C)) xor not ((A and B) or (C and B))"


from logica.BooleanConverter import BooleanConverter
from logica.TruthTableGenerator import TruthTableGenerator


if __name__ == "__main__":
    converter = BooleanConverter()
    generator = TruthTableGenerator()
    
    test_cases = [
        z,
        x,
        "A xor (B xnor C)",
        "(A and B) xnor (C xor D)"
        "A or B"
    ]
    
    for expr in test_cases:
        print(f"\n{'='*50}\nExpresión original: {expr}")
        
        try:
            # Convertir expresión
            processed = converter.convert_expression(expr)
            print(f"Expresión procesada: {processed}")
            
            # Generar tabla de verdad
            variables, truth_table = generator.generate_truth_table(processed)
            
            # Mostrar resultados
            print("\nVariables detectadas:", variables)
            print("\nTabla de verdad:")
            generator.print_truth_table(variables, truth_table)
            
        except ValueError as e:
            print(f"\nError: {str(e)}")