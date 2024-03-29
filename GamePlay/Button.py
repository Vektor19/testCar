import pygame

class Button:
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size

    def draw(self, screen):
        font = pygame.font.SysFont(None, 26)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2))
        pygame.draw.rect(screen, (60, 60, 60), (self.position[0], self.position[1], self.size[0], self.size[1]), border_radius=10)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_position):
        return (self.position[0]) < mouse_position[0] < (self.position[0] + self.size[0]) and \
               (self.position[1]) < mouse_position[1] < (self.position[1] + self.size[1])