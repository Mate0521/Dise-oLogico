from collections import deque

def codificar(ruta):
    numero=0
    with open(ruta, "rb") as imagen:
            
            while (chunk := imagen.read(1024)):  # Leer de 1024 en 1024 bytes
                print(chunk)
                for byte in chunk:
                    numero = (numero * 256) + byte
    print(numero)
    convertir_base(numero, 5000)
    return numero
def convertir_base(numero, base):
    if numero == 0:
        return "0"
    
    caracteres = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz☺♀♪♫☼►◄↕‼◙♂♪♫☼►1•↕‼¶§▬↨↑↓→←☻◘2345678↔▲()*+,-./019:;<=>?@ÉB♠7DEFGFIJKLMNOPQRS◘♦UVWYZ[\]^_`abcdefghij◙7lm"
    resultado = deque()  # Usamos deque para evitar concatenaciones costosas
    
    while numero:
        numero, residuo = divmod(numero, base)  
        resultado.appendleft(caracteres[residuo])  # Agrega al inicio de la lista
    
    return ''.join(resultado) 

codificar(r"C:\Users\MATEO CARVAJAL\Pictures\chinbaDeImagen.jpg")
