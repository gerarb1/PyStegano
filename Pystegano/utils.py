def convert_text_to_binary(text: str) -> str:
    """Convierte un string de texto a una cadena binaria."""
    return ''.join(format(ord(char), '08b') for char in text)

def convert_binary_to_text(binary_string: str) -> str:
    """
    Convierte una cadena binaria a texto con validación mejorada.
    """
    if not binary_string:
        return ""
    
    if len(binary_string) % 8 != 0:
        # Truncar a la longitud múltiplo de 8 más cercana
        binary_string = binary_string[:-(len(binary_string) % 8)]
    
    text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        try:
            ascii_value = int(byte, 2)
            
            # Validar que sea un carácter ASCII válido
            # Permitir caracteres imprimibles (32-126) y algunos especiales (9, 10, 13)
            if (32 <= ascii_value <= 126) or ascii_value in [9, 10, 13]:
                text += chr(ascii_value)
            elif ascii_value == 0:
                # Null character podría indicar fin de datos válidos
                break
            else:
                # Si encontramos un carácter no válido, podría ser ruido/corrupción
                # Opción 1: Continuar (comentar el break)
                # Opción 2: Detener aquí (mantener el break)
                break
                
        except (ValueError, OverflowError):
            # Si hay un error convirtiendo el byte, detener
            break
    
    return text

# Función adicional para debugging
def validate_binary_string(binary_string: str) -> bool:
    """
    Valida si una cadena binaria es válida.
    """
    if not binary_string:
        return False
    
    # Verificar que solo contenga 0s y 1s
    if not all(bit in '01' for bit in binary_string):
        return False
    
    # Verificar que sea múltiplo de 8
    if len(binary_string) % 8 != 0:
        return False
    
    return True