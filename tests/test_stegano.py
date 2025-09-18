import pytest
from Pystegano.core import Stegano
from PIL import Image
import os

# Archivos de prueba
@pytest.fixture
def clean_test_files():
    """Fixture para limpiar archivos de prueba después de cada test."""
    yield
    if os.path.exists("test_output.png"):
        os.remove("test_output.png")
    if os.path.exists("small_image.png"):
        os.remove("small_image.png")

@pytest.fixture
def create_test_image():
    """Crea una imagen de prueba para los tests."""
    img = Image.new('RGB', (10, 10), color = 'red')
    img.save("test_image.png")
    yield "test_image.png"
    os.remove("test_image.png")

def test_hide_and_reveal_message(create_test_image, clean_test_files):
    """Prueba que el mensaje se oculta y revela correctamente."""
    message = "Hola, mundo! Esto es una prueba de esteganografía."
    output_path = "test_output.png"
    
    Stegano.hide(create_test_image, message, output_path)
    
    assert os.path.exists(output_path)
    
    revealed_message = Stegano.reveal(output_path)
    
    assert revealed_message == message

def test_message_too_long(create_test_image, clean_test_files):
    """Prueba que se lanza un error si el mensaje es demasiado largo."""
    long_message = "a" * 500  # Mensaje largo para una imagen de 10x10 (300 bits de capacidad)
    output_path = "test_output.png"
    
    with pytest.raises(ValueError, match="El mensaje es demasiado largo para la imagen."):
        Stegano.hide(create_test_image, long_message, output_path)

def test_file_not_found():
    """Prueba que se lanza un error si la imagen no se encuentra."""
    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        Stegano.hide("non_existent_image.png", "test", "output.png")
        