
def unicode_caracteres_seguros(base):
    caracteres = []
    current = 33  # Empezar desde '!'
    while len(caracteres) < base:
        if current >= 0x10FFFF:  # Límite máximo de Unicode
            raise ValueError(f"Base {base} excede el límite de caracteres seguros disponibles.")
        # Excluir caracteres problemáticos
        if not (
            current <= 32 or          # Controles y espacio
            127 <= current <= 159 or  # Caracteres de control extendidos
            0xD800 <= current <= 0xDFFF or  # Suplentes UTF-16
            current in {0x2028, 0x2029, 0xFEFF}  # Separadores y BOM
        ):
            caracteres.append(chr(current))
        current += 1
    return ''.join(caracteres)

def base_n_to_decimal(num_str, base, caracteres):
    """Convierte un número en base N a decimal usando los caracteres especificados"""
    try:
        if base <= 10:
            # Para bases pequeñas, usar los dígitos estándar 0-9
            return int(num_str, base)
        else:
            # Para bases mayores, usar el mapeo de caracteres personalizados
            decimal_value = 0
            num_str = num_str[::-1]  # Invertir para procesar de derecha a izquierda
            for i, char in enumerate(num_str):
                try:
                    digit_value = caracteres.index(char)
                except ValueError:
                    raise ValueError(f"Carácter '{char}' no válido para base {base}")
                decimal_value += digit_value * (base ** i)
            return decimal_value
    except ValueError as e:
        print(f"Error: {e}")
        return None

def decimal_to_base_n(num, base, caracteres):
    """Convierte un número decimal a base N usando los caracteres especificados"""
    if num == 0:
        return caracteres[0]
    
    digits = []
    is_negative = False
    
    if num < 0:
        is_negative = True
        num = abs(num)
    
    while num > 0:
        remainder = num % base
        digits.append(caracteres[remainder])
        num = num // base
    
    if is_negative:
        digits.append('-')
    
    return ''.join(reversed(digits))

def calcular(operacion, num1_str, num2_str, base, caracteres):
    """Realiza operaciones aritméticas en base N"""
    # Convertir a decimal
    num1 = base_n_to_decimal(num1_str, base, caracteres)
    num2 = base_n_to_decimal(num2_str, base, caracteres)
    
    if num1 is None or num2 is None:
        return None
    
    # Realizar operación
    if operacion == '+':
        resultado = num1 + num2
    elif operacion == '-':
        resultado = num1 - num2
    elif operacion == '*':
        resultado = num1 * num2
    elif operacion == '/':
        if num2 == 0:
            print("Error: División por cero")
            return None
        resultado = num1 // num2  # División entera para bases no decimales
    else:
        print("Operación no válida")
        return None
    
    # Convertir resultado a base N
    return decimal_to_base_n(resultado, base, caracteres)

def mostrar_menu():
    print("\nCalculadora de Base N con Caracteres Unicode")
    print("1. Sumar (+)")
    print("2. Restar (-)")
    print("3. Multiplicar (*)")
    print("4. Dividir (/)")
    print("5. Salir")


while True:
    mostrar_menu()
    opcion = input("Seleccione una operación (1-5): ")
    
    if opcion == '5':
        print("Saliendo de la calculadora...")
        break
    
    if opcion not in ['1', '2', '3', '4']:
        print("Opción no válida. Intente nuevamente.")
        continue
    
    operaciones = {'1': '+', '2': '-', '3': '*', '4': '/'}
    operacion = operaciones[opcion]
    
    base = input("Ingrese la base : ")
    try:
        base = int(base)
        if base > 2 and base <= 64:
            caracteres = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        else:
            caracteres = unicode_caracteres_seguros(base)

        print(f"Caracteres para base {base}: {caracteres}")  
    except ValueError as e:
        print(f"Error: {e}")
        continue
    
    num1 = input(f"Ingrese el primer número (usar caracteres mostrados): ")
    num2 = input(f"Ingrese el segundo número (usar caracteres mostrados): ")
    
    resultado = calcular(operacion, num1, num2, base, caracteres)
    print(f"Resultado en base {base}: {resultado}")

