from collections import deque
import os

def unicode_caracteres_seguros(base):
    caracteres = []
    current = 33
    while len(caracteres) < base:
        if current >= 0x10FFFF:
            raise ValueError(f"Base {base} excede el límite de caracteres seguros.")
        if not (
            current <= 32 or
            127 <= current <= 159 or
            0xD800 <= current <= 0xDFFF or
            current in {0x2028, 0x2029, 0xFEFF}
        ):
            caracteres.append(chr(current))
        current += 1
    return ''.join(caracteres)

def convertir_a_base(numero, base, caracteres_base):
    if numero == 0:
        return caracteres_base[0]
    
    resultado = deque()
    while numero > 0:
        numero, residuo = divmod(numero, base)
        resultado.appendleft(caracteres_base[residuo])
    
    return ''.join(resultado)

def convertir_de_base(cadena, base):
    caracteres = unicode_caracteres_seguros(base)
    mapa = {c: i for i, c in enumerate(caracteres)}
    numero = 0
    for caracter in cadena:
        if caracter not in mapa:
            raise ValueError(f"Carácter '{caracter}' no válido para base {base}")
        numero = numero * base + mapa[caracter]
    return numero

def codificar(ruta_imagen, base, bloque_bytes=16):
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_imagen}")
    
    nombre_txt = f"{os.path.splitext(ruta_imagen)[0]}_{base}.txt"
    caracteres_base = unicode_caracteres_seguros(base)
    
    with open(ruta_imagen, "rb") as archivo_imagen, \
         open(nombre_txt, "w", encoding="utf-8") as archivo_txt:
        
        while True:
            chunk = archivo_imagen.read(bloque_bytes)
            if not chunk:
                break
            
            numero = int.from_bytes(chunk, byteorder='big', signed=False)
            digitos = convertir_a_base(numero, base, caracteres_base)
            archivo_txt.write(f"{len(chunk)}:{digitos}\n")
    
    return nombre_txt

def decodificar(ruta_txt, base_origen, ruta_original=None):
    if not os.path.exists(ruta_txt):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_txt}")

    caracteres_base = unicode_caracteres_seguros(base_origen)

    # Detectamos la extensión desde ruta_original (si existe)
    extension = ".bin"
    if ruta_original:
        extension = os.path.splitext(ruta_original)[1]
    nombre_salida = os.path.splitext(ruta_txt)[0] + "_decodificado" + extension

    tamano_original = None
    if ruta_original and os.path.exists(ruta_original):
        tamano_original = os.path.getsize(ruta_original)

    with open(ruta_txt, "r", encoding="utf-8") as archivo_txt, \
         open(nombre_salida, "wb") as archivo_salida:
        
        bytes_totales = bytearray()
        
        for linea in archivo_txt:
            linea = linea.strip()
            if not linea:
                continue
            
            try:
                longitud_str, datos = linea.split(":", 1)
                longitud = int(longitud_str)

                numero = convertir_de_base(datos, base_origen)
                chunk_bytes = numero.to_bytes(longitud, 'big')
                bytes_totales.extend(chunk_bytes)

            except Exception as e:
                print(f"¡Error al procesar línea! {linea}\nDetalle: {e}")
                continue
        
        if tamano_original is not None:
            bytes_totales = bytes_totales[:tamano_original]
        
        archivo_salida.write(bytes_totales)
    
    return nombre_salida

# Ejemplo de uso
if __name__ == "__main__":
    try:
        ruta_img = r"C:\Users\MATEO CARVAJAL\Pictures\chinbaDeImagen.jpg"  # Puedes cambiar a cualquier formato
        base = 2000

        archivo_codificado = codificar(ruta_img, base)
        print(f" Archivo codificado: {archivo_codificado}")
        
        archivo_decodificado = decodificar(archivo_codificado, base, ruta_original=ruta_img)
        print(f" Archivo decodificado: {archivo_decodificado}")

    except Exception as e:
        print(f" Error: {str(e)}")