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
        """
        try:
            img = Image.open(image_path)
            if img.mode not in ['RGB', 'RGBA']:
                raise ValueError("La imagen debe estar en modo RGB o RGBA.")
                
            pixels = img.load()
            
            binary_message = convert_text_to_binary(message + '###')
            
            max_capacity = img.width * img.height * 3
            if len(binary_message) > max_capacity:
                raise ValueError("El mensaje es demasiado largo para la imagen.")
            
            data_index = 0
            for x in range(img.width):
                for y in range(img.height):
                    if data_index >= len(binary_message):
                        break
                    
                    pixel = list(pixels[x, y])
                    
                    for n in range(3):
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
            raise e

    @staticmethod
    def reveal(image_path: str) -> str:
        """
        Revela un mensaje de texto oculto en una imagen.
        """
        try:
            img = Image.open(image_path)
            
            # Convertir a RGB si no lo está
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
                
            pixels = img.load()
            binary_message = ""
            terminator = '###'
            
            # Convierte el terminador a binario para buscarlo
            binary_terminator = ''.join(format(ord(char), '08b') for char in terminator)

            # Usar el mismo orden de iteración que en hide()
            for x in range(img.width):
                for y in range(img.height):
                    pixel = list(pixels[x, y])
                    
                    # Extraer el LSB de cada canal RGB (mismo orden que hide)
                    for n in range(3):
                        binary_message += str(pixel[n] & 0x01)

                        # Verificar si hemos encontrado el terminador
                        if binary_message.endswith(binary_terminator):
                            # Remover el terminador del mensaje
                            binary_message = binary_message[:-len(binary_terminator)]
                            
                            # Verificar que la longitud sea múltiplo de 8
                            if len(binary_message) % 8 != 0:
                                # Truncar al múltiplo de 8 más cercano
                                binary_message = binary_message[:-(len(binary_message) % 8)]
                            
                            # Decodificar el mensaje y retornarlo
                            message = convert_binary_to_text(binary_message)
                            return message
                
                # Si ya encontramos el mensaje, salir del bucle exterior también
                if binary_message.endswith(binary_terminator):
                    break
            
            # Si llegamos aquí, no encontramos el terminador
            # Intentar decodificar lo que tenemos si es válido
            if len(binary_message) >= 8 and len(binary_message) % 8 == 0:
                message = convert_binary_to_text(binary_message)
                return message
            else:
                return ""  # No hay mensaje válido

        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo en la ruta {image_path}")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
            raise e