"""
Submódulo con funciones de utilidad para la conversión de datos.
"""

def convert_text_to_binary(text: str) -> str:
    """Convierte una cadena de texto a una cadena de bits."""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def convert_binary_to_text(binary_string: str) -> str:
    """Convierte una cadena de bits a una cadena de texto."""
    text = ''
    i = 0
    while i < len(binary_string):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
        i += 8
    return text