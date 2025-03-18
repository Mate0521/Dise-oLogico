from collections import deque

def convertir_base(numero, base):
    if numero == 0:
        return "0"
    
    caracteres = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz☺♀♪♫☼►◄↕‼◙♂♪♫☼►1•↕‼¶§▬↨↑↓→←☻◘↔▲()*+,-./0123456789:;<=>?@ÉB♠7DEFGFIJKLMNOPQRS◘♦UVWYZ[\]^_`abcdefghij◙7lm"
    resultado = deque()  # Usamos deque para evitar concatenaciones costosas
    
    while numero:
        numero, residuo = divmod(numero, base)  # Obtiene cociente y residuo en una sola operación
        resultado.appendleft(caracteres[residuo])  # Agrega al inicio de la lista
    
    return ''.join(resultado)  # Une los caracteres en una sola operación eficiente

# Ejemplo de uso:
numero_decimal =1556
base_destino = 16
print(f"{numero_decimal} en base {base_destino} es: {convertir_base(numero_decimal, base_destino)}")


