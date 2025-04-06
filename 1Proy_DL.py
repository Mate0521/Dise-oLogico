from collections import deque  # Importa deque para manejar secuencias de caracteres
import os  # Importa os para manejo de archivos
import matplotlib.pyplot as plt  # Importa matplotlib para mostrar imágenes
import matplotlib.image as mpimg  # Importa mpimg para leer imágenes

def codificar(ruta_imagen, base):
    # Crear archivo .txt 
    nombre_txt = os.path.splitext(ruta_imagen)[0] + f"{base}.txt"
    
    # Generar caracteres seguros para la base
    caracteres_base = unicode_caracteres_seguros(base)
    
    with open(ruta_imagen, "rb") as archivo_imagen, open(nombre_txt, "w", encoding="utf-8") as archivo_txt:
        while True:
            # Leer 16 bytes (128 bits) por bloque
            chunk = archivo_imagen.read(16)
                
            if not chunk:
                break  # Fin del archivo
            
            # Rellenar con ceros si el chunk es menor a 4 bytes
            if len(chunk) < 16:
                chunk += b'\x00' * (16 - len(chunk))
            
            numero = int.from_bytes(chunk, byteorder='big', signed=False)
            
            # Convertir el número a la base especificada
            digitos = convertir_a_base(numero, base, caracteres_base)
            
            # Escribir los dígitos en el archivo .txt
            archivo_txt.write(f"{digitos}\n")

def decodificar(ruta_txt, base_origen, base_destino):
    if not os.path.exists(ruta_txt):  # Verifica si el archivo de texto existe
        print(f"Error: No se encontró {ruta_txt}.")
        return
    caracteres_base = unicode_caracteres_seguros(base_destino)
      

    nombre_txt_salida = os.path.splitext(ruta_txt)[0] + f"decodificado{base_destino}.txt"  # Nombre del archivo de salida

    with open(ruta_txt, "r", encoding="utf-8") as archivo_txt, open(nombre_txt_salida, "w", encoding="utf-8") as archivo_salida:
        for linea in archivo_txt:
            linea = linea.strip()  # Elimina espacios en blanco
            numero = convertir_de_base(linea, base_origen)  # Convierte de la base original a decimal
            digitos_convertidos = convertir_a_base(numero, base_destino,caracteres_base)  # Convierte a la nueva base de salida
            archivo_salida.write(f"{digitos_convertidos}\n")  # Escribe el número en la nueva base

def convertir_a_base(numero, base, caracteres_base):
    
    if numero == 0:
        return caracteres_base[0]  
    
    resultado = deque()
    while numero > 0:
        numero, residuo = divmod(numero, base)
        resultado.appendleft(caracteres_base[residuo])
    
    return ''.join(resultado)


def convertir_de_base(cadena, base):
    caracteres = unicode_caracteres_seguros(base)  # Obtiene los caracteres de la base
    mapa = {c: i for i, c in enumerate(caracteres)}  # Crea un diccionario con los valores de cada caracter
    numero = 0  # Inicializa el número decimal

    for caracter in cadena:
        numero = numero * base + mapa[caracter]  # Convierte la cadena a un número decimal

    return numero  # Retorna el número en decimal

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

def mostrar_imagen(ruta_imagen):
    if os.path.exists(ruta_imagen):  # Verifica si la imagen existe
        img = mpimg.imread(ruta_imagen)  # Lee la imagen
        plt.imshow(img)  # Muestra la imagen
        plt.axis('off')  # Oculta los ejes
        plt.show()  # Muestra la imagen en pantalla
    else:
        print(f"Error: No se encontró la imagen {ruta_imagen}.")

# Ejemplo de uso
codificar(r"/home/estudiante/Descargas/inkscape.app/wp-content/uploads/imagen-vectorial.webp", 2000)  # Codifica la imagen en base 64
if os.path.exists(r"/home/estudiante/Descargas/inkscape.app/wp-content/uploads/imagen-vectorial2000.txt"):  # Verifica si el archivo codificado existe
    decodificar(r"/home/estudiante/Descargas/inkscape.app/wp-content/uploads/imagen-vectorial2000.txt", 2000, 5000)  # Decodifica el archivo a base 1000
    mostrar_imagen(r"/home/estudiante/Descargas/inkscape.app/wp-content/uploads/imagen-vectorial.webp")
    
else:
    print("Error: No se encontró el archivo de texto generado.")