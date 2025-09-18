"""
Módulo principal para la librería de esteganografía.
Contiene la clase Stegano para ocultar y revelar mensajes.
"""

from PIL import Image
from .utils import convert_text_to_binary, convert_binary_to_text

class Stegano:
    """
    Una clase para realizar esteganografía LSB en imágenes.
    """
    
    @staticmethod
    def hide(image_path: str, message: str, output_path: str) -> None:
        """
        Oculta un mensaje de texto en una imagen PNG.

        Args:
            image_path: Ruta a la imagen original (solo formato PNG).
            message: El mensaje de texto a ocultar.
            output_path: La ruta donde se guardará la imagen modificada.
            
        Raises:
            ValueError: Si el mensaje es demasiado largo para la imagen.
            FileNotFoundError: Si la imagen no se encuentra.
        """
        try:
            img = Image.open(image_path)
            if img.mode != 'RGB' and img.mode != 'RGBA':
                raise ValueError("La imagen debe estar en modo RGB o RGBA.")
                
            pixels = img.load()
            
            # Un terminador especial para indicar el final del mensaje.
            # Convertimos el mensaje a binario.
            binary_message = convert_text_to_binary(message + '###')
            
            # Calcular la capacidad máxima de la imagen.
            max_capacity = img.width * img.height * 3
            if len(binary_message) > max_capacity:
                raise ValueError("El mensaje es demasiado largo para la imagen.")
            
            data_index = 0
            for x in range(img.width):
                for y in range(img.height):
                    if data_index >= len(binary_message):
                        break
                    
                    pixel = list(pixels[x, y])
                    
                    for n in range(3): # Modificar los canales R, G, B
                        if data_index < len(binary_message):
                            bit = int(binary_message[data_index])
                            pixel[n] = (pixel[n] & 0xFE) | bit
                            data_index += 1
                    
                    pixels[x, y] = tuple(pixel)
                
                if data_index >= len(binary_message):
                    break
            
            img.save(output_path, "PNG")
            print(f"Mensaje oculto con éxito en {output_path}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo en la ruta {image_path}")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")


    @staticmethod
    def reveal(image_path: str) -> str:
        """
        Revela un mensaje de texto oculto en una imagen.

        Args:
            image_path: Ruta a la imagen que contiene el mensaje.

        Returns:
            El mensaje de texto revelado.
            
        Raises:
            FileNotFoundError: Si la imagen no se encuentra.
        """
        try:
            img = Image.open(image_path)
            pixels = img.load()
            
            binary_message = ""
            for x in range(img.width):
                for y in range(img.height):
                    pixel = list(pixels[x, y])
                    
                    for n in range(3):
                        binary_message += str(pixel[n] & 0x01)
                    
                    # Comprobamos si el terminador está en los últimos 16 bits.
                    if '1111111111111110' in binary_message:
                        break
                
                if '1111111111111110' in binary_message:
                    break
            
            # Eliminamos el terminador del mensaje binario.
            binary_message = binary_message.split('1111111111111110')[0]
            
            # Convertimos el binario de nuevo a texto.
            message = convert_binary_to_text(binary_message)
            
            return message

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo en la ruta {image_path}")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
            return ""
        