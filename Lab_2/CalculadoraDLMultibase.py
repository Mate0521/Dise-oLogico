def generar_alfabeto():
    digitos = [str(i) for i in range(10)]
    mayusculas = [chr(i) for i in range(65, 78)] + ['Ñ'] + [chr(i) for i in range(78, 91)]
    minusculas = [chr(i) for i in range(97, 110)] + ['ñ'] + [chr(i) for i in range(110, 123)]
    letras = digitos + mayusculas + minusculas
    extendido = letras[:]
    while len(extendido) < 5000:
        for c1 in letras:
            for c2 in letras:
                extendido.append(c1 + c2)
                if len(extendido) >= 5000:
                    break
            if len(extendido) >= 5000:
                break
    return extendido

ALFABETO = generar_alfabeto()
MAPA_SIMBOLO_A_VALOR = {s: i for i, s in enumerate(ALFABETO)}
MAPA_VALOR_A_SIMBOLO = {i: s for i, s in enumerate(ALFABETO)}

def base_n_a_decimal(valor, base):
    base = int(base)
    valor = valor.strip()
    unidades = []

    # Si la base es mayor que 62, tratamos las combinaciones de símbolos
    if base > 62:
        # Aquí separamos los valores por guión si son combinaciones
        unidades = valor.split('-')  # símbolos separados por guiones
    else:
        valor = valor.replace("-", "")  # quitar guiones decorativos
        unidades = list(valor)

    resultado = 0
    for exp, digito in enumerate(reversed(unidades)):
        val = MAPA_SIMBOLO_A_VALOR.get(digito)
        if val is None or val >= base:
            raise ValueError(f"Dígito inválido '{digito}' para base {base}")
        resultado += val * (base ** exp)
    return resultado

def decimal_a_base_n(numero, base):
    base = int(base)
    if numero == 0:
        return ALFABETO[0]
    resultado = []
    negativo = numero < 0
    numero = abs(numero)
    while numero > 0:
        resultado.append(MAPA_VALOR_A_SIMBOLO[numero % base])
        numero //= base
    signo = '-' if negativo else ''
    if base > 62:
        return signo + '-'.join(reversed(resultado))
    return signo + ''.join(reversed(resultado))


def mostrar_paso_a_paso(valor1, valor2, base, operacion):
    base = int(base)

    if base > 62:
        val1 = valor1.split('-')
        val2 = valor2.split('-')
    else:
        val1 = list(valor1.replace('-', ''))
        val2 = list(valor2.replace('-', ''))

    len_max = max(len(val1), len(val2))
    val1 = ["0"] * (len_max - len(val1)) + val1
    val2 = ["0"] * (len_max - len(val2)) + val2

    carry = 0
    resultado = []

    print("\nPaso a paso detallado:")

    # Comparamos los valores en decimal para ver si el resultado será negativo
    decimal1 = base_n_a_decimal(valor1, base)
    decimal2 = base_n_a_decimal(valor2, base)

    if operacion == '-' and decimal1 < decimal2:
        print("El resultado será negativo; se intercambian los valores para mostrar la resta.")
        val1, val2 = val2, val1
        negativo = True
    else:
        negativo = False

    for i in range(len_max - 1, -1, -1):
        d1 = MAPA_SIMBOLO_A_VALOR[val1[i]]
        d2 = MAPA_SIMBOLO_A_VALOR[val2[i]]

        if operacion == '+':
            suma = d1 + d2 + carry
            carry = suma // base
            resultado.append(MAPA_VALOR_A_SIMBOLO[suma % base])
            print(f"{val1[i]} + {val2[i]} = {MAPA_VALOR_A_SIMBOLO[suma % base]} (se lleva {carry})")
        else:
            d1 -= carry
            if d1 < d2:
                d1 += base
                carry = 1
                prestamo = "sí"
            else:
                carry = 0
                prestamo = "no"
            resta = d1 - d2
            resultado.append(MAPA_VALOR_A_SIMBOLO[resta])
            print(f"{val1[i]} - {val2[i]} = {MAPA_VALOR_A_SIMBOLO[resta]} (pide prestado: {prestamo})")

    if operacion == '+' and carry:
        resultado.append(MAPA_VALOR_A_SIMBOLO[carry])
        print(f"Se lleva {carry}, añadiendo al final: {MAPA_VALOR_A_SIMBOLO[carry]}")

    resultado.reverse()

    # Volver a unir usando "-" si la base es mayor a 62
    resultado_str = '-'.join(resultado) if base > 62 else ''.join(resultado)
    if operacion == '-' and negativo:
        resultado_str = '-' + resultado_str

    print(f"\nResultado: {resultado_str}")


def realizar_operacion_paso_a_paso(valor1, valor2, base, operacion):
    base = int(base)
    dec1 = base_n_a_decimal(valor1, base)
    dec2 = base_n_a_decimal(valor2, base)

    print(f"\nOperación en base {base}:")
    print(f"{valor1} ({dec1}) {operacion} {valor2} ({dec2})")

    if operacion == '+':
        resultado = dec1 + dec2
    else:
        resultado = dec1 - dec2

    resultado_base = decimal_a_base_n(resultado, base)
    print(f"\nResultado en decimal: {resultado}")
    print(f"Resultado en base {base}: {resultado_base}")

    mostrar_paso_a_paso(valor1, valor2, base, operacion)

    return resultado

def calculadora_multibase():
    print("=== Calculadora Multibase ===")
    bases_usadas = []

    valor = input("Ingrese el primer número (use '-' como separador si base >62): ").strip()
    base = int(input("Ingrese la base de ese número: ").strip())
    resultado = base_n_a_decimal(valor, base)
    bases_usadas.append(base)

    while True:
        cont = input("¿Desea agregar otro número? (s/n): ").strip().lower()
        if cont != 's':
            break
        operacion = input("Ingrese la operación (+ o -): ").strip()
        if operacion not in ['+', '-']:
            print("Operación inválida, use '+' o '-'.")
            continue
        valor2 = input("Ingrese el siguiente número (use '-' como separador si base >62): ").strip()
        base2 = int(input("Ingrese la base de ese número: ").strip())

        if base2 == base:
            resultado = realizar_operacion_paso_a_paso(decimal_a_base_n(resultado, base), valor2, base, operacion)
        else:
            dec2 = base_n_a_decimal(valor2, base2)
            if operacion == '+':
                resultado += dec2
            else:
                resultado -= dec2
        if base2 not in bases_usadas:
            bases_usadas.append(base2)

    print("\n=== Resultado Final ===")
    print(f"Base 10: {resultado}")
    for b in bases_usadas:
        print(f"Base {b}: {decimal_a_base_n(resultado, b)}")

if __name__ == "__main__":
    calculadora_multibase()
