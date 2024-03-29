import pygame
class MenuItem:
    """
    Represents a clickable menu item in a pygame application.

    Attributes:
        caption (str): The text displayed on the menu item.
        position (tuple): The position (x, y) of the menu item on the screen.
        function (function): The function to be executed when the menu item is clicked.
        rect (pygame.Rect): A rectangle representing the boundaries of the menu item.
        font (pygame.font.Font): The font used for rendering the caption.
        text_color (tuple): The color of the text on the menu item.
        img (pygame.Surface): The surface representing the graphical appearance of the menu item.
    """
    def __init__(self,caption,position,function,size=(300,100)):
        """
        Initializes a MenuItem object.

        Args:
            caption (str): The text to be displayed on the menu item.
            position (tuple): The position (x, y) of the menu item on the screen.
            function (function): The function to be executed when the menu item is clicked.
            size (tuple, optional): The size (width, height) of the menu item. Defaults to (300, 100).
        """
        self.caption = caption
        self.position = position
        self.rect = pygame.Rect(position, size)
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (10, 10, 10,255)
        self.img = pygame.image.load("resources/images/buttons/btn.png")
        self.function=function
    def draw(self, surface):
        """
        Draws the menu item on the given surface.

        Args:
            surface (pygame.Surface): The surface onto which the menu item will be drawn.
        """
        self.draw_caption()
        surface.blit(self.img, self.position)
    def draw_caption(self):
        """Draws the caption text on the menu item."""
        text_surface = self.font.render(self.caption, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.img.get_rect().center)
        self.img.blit(text_surface, text_rect)
    def is_clicked(self, pos):
        """
        Checks if the menu item is clicked at the given position.

        Args:
            pos (tuple): The position (x, y) of the click.

        Returns:
            bool: True if the menu item is clicked, False otherwise.
        """
        return self.rect.collidepoint(pos)
    def action(self):
        """Executes the function associated with the menu item."""
        self.function()

