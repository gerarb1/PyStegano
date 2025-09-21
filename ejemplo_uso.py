#!/usr/bin/env python3
"""
Ejemplo simple de uso de PyStegano
"""

from PyStegano.core import Stegano
from PIL import Image
import os

def main():
    print("=== EJEMPLO SIMPLE DE PYSTEGANOGRAFIA ===\n")
    
    # 1. Crear imagen de prueba si no existe
    imagen_original = "test_image.png"
    if not os.path.exists(imagen_original):
        print("Creando imagen de prueba...")
        img = Image.new('RGB', (100, 100), color='lightblue')
        img.save(imagen_original)
        print(f" Imagen creada: {imagen_original}")
    
    # 2. Configuración
    mensaje = "pokemon red."
    imagen_salida = "mensaje_oculto.png"
    
    print(f" Mensaje: '{mensaje}'")
    print(f" Imagen original: {imagen_original}")
    print(f" Imagen de salida: {imagen_salida}")
    
    # 3. Ocultar mensaje
    print("\n Ocultando mensaje...")
    try:
        Stegano.hide(imagen_original, mensaje, imagen_salida)
        print(" Mensaje ocultado exitosamente")
        
        # Verificar que ambas imágenes existen
        print(f"Original existe: {os.path.exists(imagen_original)}")
        print(f"Con mensaje existe: {os.path.exists(imagen_salida)}")
        
    except Exception as e:
        print(f" Error ocultando: {e}")
        return
    
    # 4. Revelar mensaje
    print("\n Revelando mensaje...")
    try:
        mensaje_revelado = Stegano.reveal(imagen_salida)
        print(f" Mensaje revelado: '{mensaje_revelado}'")
        
        # Verificar si coincide
        if mensaje_revelado == mensaje:
            print("🎉 ¡Éxito! Los mensajes coinciden perfectamente.")
        else:
            print("⚠️ Los mensajes no coinciden exactamente:")
            print(f"  Original:  '{mensaje}'")
            print(f"  Revelado:  '{mensaje_revelado}'")
            
    except Exception as e:
        print(f" Error revelando: {e}")

if __name__ == "__main__":
    main()