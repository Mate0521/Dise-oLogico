from collections import deque
import os

def codificar(ruta_imagen, base):
    # Crear archivo .txt 
    nombre_txt = os.path.splitext(ruta_imagen)[0] + f"{base}.txt"
    
    with open(ruta_imagen, "rb") as archivo_imagen, open(nombre_txt, "w", encoding="utf-8") as archivo_txt:
        while True:
            # Leer 4 bytes (32 bits) por bloque
            chunk = archivo_imagen.read(16)
            if not chunk:
                break  # Fin del archivo

            numero = int.from_bytes(chunk, byteorder='big', signed=False)
            
            # invocamos el metodo convertir_a_base para convertir el número a la base especificada
            digitos = convertir_a_base(numero, base)
            
            # Escribir los dígitos en el archivo .txt
            archivo_txt.write(f"{digitos}\n")

def convertir_a_base(numero, base):
    if numero == 0:
        return "0"
    
    caracteres = unicode(base)
    resultado = deque()
    
    while numero > 0:
        numero, residuo = divmod(numero, base)
        resultado.appendleft(caracteres[residuo])
    
    return ''.join(resultado)

def unicode(cantidad):
    # Genera caracteres Unicode hasta el límite especificado
    return [chr(i) for i in range(min(cantidad, 0x10FFFF + 1))]
 


codificar(r"C:\Users\MATEO CARVAJAL\Pictures\Kimetsu.webp", 5000)
    
