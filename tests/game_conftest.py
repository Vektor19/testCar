import os
import pytest
import tempfile
from PIL import Image

@pytest.fixture(autouse=True)
def prepare_image():
    width = 512
    height = 512
    test_texture = generate_test_texture(width, height)
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:  # зміна тут
        test_texture.save(tmp_file.name)
        # Ось ви можете використовувати tmp_file.name, щоб вказати шлях до тимчасового файлу
        yield tmp_file.name

    # Не забудьте закрити тимчасовий файл
    os.unlink(tmp_file.name)  # Видалення файлу після тесту

def generate_test_texture(width, height):
    image = Image.new("RGB", (width, height), color="black")

    for y in range(height):
        for x in range(width):
            r = (x * 255) // width
            g = (y * 255) // height
            b = 128
            image.putpixel((x, y), (r, g, b))

    return image


@pytest.fixture(autouse=True)
def prepare_text_file():
    text_content = generate_test_text()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        tmp_file.write(text_content)
        yield tmp_file.name

    os.unlink(tmp_file.name)

def generate_test_text():
    # Generate some test text content
    return "This is a test text file.\nIt contains some sample text for testing purposes."

@pytest.fixture
def prepare_tmp_file(request):
    format = request.param
    with tempfile.NamedTemporaryFile(mode='w', suffix='.'+ format, delete=False) as tmp_file:
        yield tmp_file.name

    os.unlink(tmp_file.name)

@pytest.fixture
def unexist_path():
    # Назва файлу
    image_name = "unexist_image.png"

    # Повний шлях до поточного робочого каталогу
    current_directory = os.getcwd()

    # Створення повного шляху до файлу
    image_path = os.path.join(current_directory, image_name)
    return image_path