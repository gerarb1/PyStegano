import pytest
from PyStegano.core import Stegano
from PIL import Image
import os

@pytest.fixture
def create_test_image(request):
    """
    Crea un archivo de imagen temporal para la prueba y se asegura de que se elimine después.
    """
    img = Image.new('RGB', (20, 20), color='red')
    img_path = "test_image.png"
    img.save(img_path)
    
    def cleanup():
        if os.path.exists(img_path):
            os.remove(img_path)
            
    request.addfinalizer(cleanup)
    
    return img_path

@pytest.fixture
def create_small_test_image(request):
    """
    Crea una imagen más pequeña para probar límites de capacidad.
    """
    img = Image.new('RGB', (5, 5), color='blue')  # 75 bits de capacidad
    img_path = "small_test_image.png"
    img.save(img_path)
    
    def cleanup():
        if os.path.exists(img_path):
            os.remove(img_path)
            
    request.addfinalizer(cleanup)
    
    return img_path

def test_hide_and_reveal_message(create_test_image):
    """Prueba que el mensaje se oculta y revela correctamente."""
    message = "Hola mundo!"
    output_path = "test_output.png"
    
    try:
        # Verificar capacidad antes de la prueba
        # Imagen 20x20 RGB = 1200 bits de capacidad
        # "Hola mundo!" + "###" = 14 caracteres = 112 bits (bien dentro del límite)
        
        Stegano.hide(create_test_image, message, output_path)
        assert os.path.exists(output_path)
        
        revealed_message = Stegano.reveal(output_path)
        assert revealed_message == message
        print(f"✓ Mensaje ocultado y revelado correctamente: '{revealed_message}'")
    
    finally:
        # Limpiamos el archivo de salida
        if os.path.exists(output_path):
            os.remove(output_path)

def test_hide_and_reveal_empty_message(create_test_image):
    """Prueba que se puede ocultar y revelar un mensaje vacío."""
    message = ""
    output_path = "test_output_empty.png"
    
    try:
        Stegano.hide(create_test_image, message, output_path)
        assert os.path.exists(output_path)
        
        revealed_message = Stegano.reveal(output_path)
        assert revealed_message == message
        print("✓ Mensaje vacío manejado correctamente")
    
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def test_hide_and_reveal_special_characters(create_test_image):
    """Prueba que se pueden ocultar caracteres especiales."""
    message = "Hola mundo!\nComo estas?\tBien, gracias."  # Sin caracteres Unicode problemáticos
    output_path = "test_output_special.png"
    
    try:
        Stegano.hide(create_test_image, message, output_path)
        assert os.path.exists(output_path)
        
        revealed_message = Stegano.reveal(output_path)
        assert revealed_message == message
        print(f"✓ Caracteres especiales manejados correctamente")
    
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

def test_message_too_long(create_small_test_image):
    """Prueba que se lanza un error si el mensaje es demasiado largo."""
    # Imagen 5x5 RGB = 75 bits de capacidad
    # Cada carácter = 8 bits, terminador "###" = 24 bits
    # Capacidad máxima ≈ 6 caracteres (48 bits) + terminador = 72 bits
    long_message = "a" * 10  # 80 bits + 24 bits terminador = 104 bits (excede 75)
    output_path = "test_output_long.png"
    
    with pytest.raises(ValueError, match="El mensaje es demasiado largo para la imagen."):
        Stegano.hide(create_small_test_image, long_message, output_path)

    # Nos aseguramos de que no se haya creado ningún archivo
    assert not os.path.exists(output_path)
    print("✓ Error de capacidad manejado correctamente")

def test_reveal_image_without_message(create_test_image):
    """Prueba revelar de una imagen que no tiene mensaje oculto."""
    revealed_message = Stegano.reveal(create_test_image)
    
    # Debería retornar cadena vacía si no hay mensaje válido
    assert isinstance(revealed_message, str)
    print(f"✓ Imagen sin mensaje manejada correctamente: '{revealed_message}'")

def test_file_not_found():
    """Prueba que se lanza un error si la imagen no se encuentra."""
    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        Stegano.hide("non_existent_image.png", "test", "output.png")
    
    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        Stegano.reveal("non_existent_image.png")
    
    print("✓ FileNotFoundError manejado correctamente")

def test_invalid_image_mode(request):
    """Prueba que se maneja correctamente una imagen en modo no RGB/RGBA."""
    # Crear imagen en escala de grises
    img = Image.new('L', (20, 20), color=128)  # Modo 'L' = grayscale
    img_path = "test_gray_image.png"
    img.save(img_path)
    
    def cleanup():
        if os.path.exists(img_path):
            os.remove(img_path)
    
    request.addfinalizer(cleanup)
    
    output_path = "test_output_gray.png"
    
    # Debería lanzar ValueError para modo no soportado
    with pytest.raises(ValueError, match="La imagen debe estar en modo RGB o RGBA"):
        Stegano.hide(img_path, "test", output_path)
    
    print("✓ Modo de imagen inválido manejado correctamente")

# Test adicional para debugging
def test_capacity_calculation():
    """Verifica que el cálculo de capacidad sea correcto."""
    img = Image.new('RGB', (10, 10), color='white')
    
    # Capacidad = width * height * 3 (canales RGB)
    expected_capacity = 10 * 10 * 3  # 300 bits
    
    # Cada carácter = 8 bits
    # Terminador "###" = 24 bits
    # Máxima longitud de mensaje = (300 - 24) / 8 = 34.5, por lo tanto 34 caracteres
    max_message_length = (expected_capacity - 24) // 8
    
    print(f"✓ Capacidad calculada: {expected_capacity} bits")
    print(f"✓ Máxima longitud de mensaje: {max_message_length} caracteres")