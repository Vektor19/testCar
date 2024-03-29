import os
import pygame

class ImagesUtils:
    @staticmethod
    def load_image(image_path):
        if not os.path.exists(image_path):
            raise FileExistsError(f"The file '{image_path}' does not exist.")
        
        if not ImagesUtils.is_image_file(image_path):
            raise ValueError("Incorrect image format.")
        
        im = None
        with open(image_path, 'rb') as fd:
            im = pygame.image.load(fd)
        return im

    @staticmethod
    def is_image_file(file_path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in image_extensions