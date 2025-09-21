# ejemplo_uso.py
from PyStegano.core import Stegano
import os

# --- Parte 1: Ocultar un mensaje ---
print("--- Ocultando el mensaje ---")
imagen_original = "test_image.png"
mensaje_secreto = "Hola mundo."
imagen_con_mensaje = "imagen_con_mensaje.png"

try:
    # Oculta el mensaje en la imagen
    Stegano.hide(imagen_original, mensaje_secreto, imagen_con_mensaje)
    
    if os.path.exists(imagen_con_mensaje):
        print(f"El mensaje ha sido ocultado con éxito en '{imagen_con_mensaje}'.")
    else:
        print("Error: No se pudo crear la imagen de salida.")
        
except FileNotFoundError as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Error: {e}")

print("\n--- ¡Comparación de Imágenes! ---")
print("Puedes abrir la imagen original y la nueva. Verás que son visualmente idénticas.")

# --- Parte 2: Revelar el mensaje ---
print("\n--- Revelando el mensaje ---")
if os.path.exists(imagen_con_mensaje):
    try:
        mensaje_revelado = Stegano.reveal(imagen_con_mensaje)
        print(f"Mensaje revelado: '{mensaje_revelado}'")
    except FileNotFoundError as e:
        print(f"Error: {e}")
else:
    print("La imagen con el mensaje no se encontró, no se puede revelar.")
    