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

def base_n_a_decimal(valor, base):
    base = int(base)
    valor = valor.strip()
    alfabeto = MAPA_SIMBOLO_A_VALOR
    unidades = []
    if base > 62:
        i = 0
        while i < len(valor):
            if valor[i] == '-':  # saltar separadores
                i += 1
                continue
            # intento de dígito de 2 caracteres
            if i + 2 <= len(valor) and valor[i:i+2] in alfabeto:
                unidades.append(valor[i:i+2])
                i += 2
            elif valor[i] in alfabeto:
                unidades.append(valor[i])
                i += 1
            else:
                raise ValueError(f"Dígito '{valor[i]}' inválido para base {base}")
    else:
        unidades = list(valor)
    resultado = 0
    for exp, digito in enumerate(reversed(unidades)):
        val = alfabeto.get(digito)
        if val is None or val >= base:
            raise ValueError(f"Dígito '{digito}' inválido para base {base}")
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
        resultado.append(ALFABETO[numero % base])
        numero //= base
    signo = '-' if negativo else ''
    if base > 62:
        return signo + '-'.join(reversed(resultado))
    return signo + ''.join(reversed(resultado))

def calculadora_multibase():
    print("=== Calculadora Multibase ===")
    resultado = 0
    bases_usadas = []
    valor = input("Ingrese el primer número: ").strip()
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
        valor = input("Ingrese el siguiente número: ").strip()
        base = int(input("Ingrese la base de ese número: ").strip())
        dec = base_n_a_decimal(valor, base)
        if operacion == '+':
            resultado += dec
        else:
            resultado -= dec
        if base not in bases_usadas:
            bases_usadas.append(base)
    print("\n=== Resultado Final ===")
    print(f"Base 10: {resultado}")
    for b in bases_usadas:
        print(f"Base {b}: {decimal_a_base_n(resultado, b)}")

if __name__ == "__main__":
    calculadora_multibase()