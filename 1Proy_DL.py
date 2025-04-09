from collections import deque
import os

def unicode_caracteres_seguros(base):
    """Genera caracteres Unicode seguros excluyendo controles y espacios"""
    caracteres = []
    current = 33  # Empezar desde '!'
    while len(caracteres) < base:
        if current >= 0x10FFFF:  # Límite máximo de Unicode
            raise ValueError(f"Base {base} excede el límite de caracteres seguros.")
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

def convertir_a_base(numero, base, caracteres_base):
    """Convierte un número decimal a otra base usando caracteres seguros"""
    if numero == 0:
        return caracteres_base[0]
    
    resultado = deque()
    while numero > 0:
        numero, residuo = divmod(numero, base)
        resultado.appendleft(caracteres_base[residuo])
    
    return ''.join(resultado)

def convertir_de_base(cadena, base):
    """Convierte una cadena en cierta base a número decimal"""
    caracteres = unicode_caracteres_seguros(base)
    mapa = {c: i for i, c in enumerate(caracteres)}
    numero = 0
    
    for caracter in cadena:
        if caracter not in mapa:
            raise ValueError(f"Carácter '{caracter}' no válido para base {base}")
        numero = numero * base + mapa[caracter]
    
    return numero

def codificar(ruta_imagen, base, bloque_bytes=16):
    """Codifica una imagen a un archivo de texto en la base especificada"""
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_imagen}")
    
    nombre_txt = f"{os.path.splitext(ruta_imagen)[0]}{base}.txt"
    caracteres_base = unicode_caracteres_seguros(base)
    
    with open(ruta_imagen, "rb") as archivo_imagen, \
         open(nombre_txt, "w", encoding="utf-8") as archivo_txt:
        
        while True:
            chunk = archivo_imagen.read(bloque_bytes)
            if not chunk:
                break
            
            # Rellenar con ceros si es necesario
            if len(chunk) < bloque_bytes:
                chunk += b'\x00' * (bloque_bytes - len(chunk))
            
            numero = int.from_bytes(chunk, byteorder='big', signed=False)
            digitos = convertir_a_base(numero, base, caracteres_base)
            archivo_txt.write(f"{digitos}\n")
    
    return nombre_txt

def decodificar(ruta_txt, base_origen, base_destino=256, bloque_bytes=16):
    """Decodifica un archivo de texto a bytes en la base destino"""
    if not os.path.exists(ruta_txt):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_txt}")
    
    # Extraer nombre base sin extensión
    nombre_base = os.path.splitext(ruta_txt)[0]
    if nombre_base.endswith(str(base_origen)):
        nombre_base = nombre_base[:-len(str(base_origen))]
    
    nombre_salida = f"{nombre_base}_decodificado.png"
    caracteres_base = unicode_caracteres_seguros(base_origen)
    
    with open(ruta_txt, "r", encoding="utf-8") as archivo_txt, \
         open(nombre_salida, "wb") as archivo_salida:
        
        for linea in archivo_txt:
            linea = linea.strip()
            if not linea:
                continue
            
            try:
                numero = convertir_de_base(linea, base_origen)
                bytes_bloque = numero.to_bytes(bloque_bytes, byteorder='big')
                archivo_salida.write(bytes_bloque)
            except ValueError as e:
                print(f"Error procesando línea: {linea} - {str(e)}")
                continue
    
    return nombre_salida

# Ejemplo de uso
if __name__ == "__main__":
    try:
        # Codificar
        archivo_codificado = codificar(r"C:\Users\MATEO CARVAJAL\Pictures\Kimetsu.webp", 2000)
        print(f"Archivo codificado creado: {archivo_codificado}")
        
        # Decodificar
        archivo_decodificado = decodificar(archivo_codificado, 2000)
        print(f"Archivo decodificado creado: {archivo_decodificado}")
        
    except Exception as e:
        print(f"Error: {str(e)}")