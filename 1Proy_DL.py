from collections import deque

def codificar(ruta):
    numero=0
    with open(ruta, "rb") as imagen:
            
            while (chunk := imagen.read(1024)):  # Leer de 1024 en 1024 bytes
                print(chunk)
                for byte in chunk:
                    numero = numero * 256 + byte  # Desplaza 8 bits y suma el byte
    print(numero)
    convertir_base(numero, 10000)
    return numero
def convertir_base(numero, base): 
    if numero == 0:
        return "0"
    
    caracteres = Unicode(base)
    resultado = deque()  # Usamos deque para evitar concatenaciones costosas 
    
    while numero:
        numero, residuo = divmod(numero, base)  
        resultado.appendleft(caracteres[residuo])  # Agrega al inicio de la lista
    
    print(resultado)
    return ''.join(resultado) 
def Unicode(cantidad):
<<<<<<< HEAD
    if cantidad > 100000:
        raise ValueError("La cantidad máxima permitida es 7000 caracteres.")
=======
>>>>>>> origin/main
    
    caracteres = [chr(i) for i in range(cantidad)]  # Genera los primeros caracteres Unicode
    return ''.join(caracteres)

codificar(r"C:\Users\MATEO CARVAJAL\Pictures\chinbaDeImagen.jpg")
    
