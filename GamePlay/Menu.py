import pygame
from GamePlay.MenuItem import MenuItem
class Menu:
    """
    Represents a menu screen in a pygame game.

    Attributes:
        menu_items (list): A list containing MenuItem objects representing the menu options.
        menu_surface (pygame.Surface): The surface representing the background of the menu.
        is_drawn (bool): Indicates whether the menu has been drawn on the screen.
    """
    def __init__(self,resume_game,restart_game,quit_game):
        """
        Initializes a Menu object.

        Args:
            resume_game (function): The function to be executed when the 'Continue' option is selected.
            restart_game (function): The function to be executed when the 'Restart' option is selected.
            quit_game (function): The function to be executed when the 'Exit' option is selected.
        """
        self.menu_items = []
        self.add_menu_item("Continue", (250, 100),resume_game)
        self.add_menu_item("Restart", (250, 250),restart_game)
        self.add_menu_item("Exit", (250, 400),quit_game)
        self.menu_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
        self.menu_surface.fill((0, 0, 0, 100))
        self.is_drawn=False
    def add_menu_item(self, caption, position,function):
        """
        Adds a menu item to the menu.

        Args:
            caption (str): The text to be displayed on the menu item.
            position (tuple): The position (x, y) of the menu item on the screen.
            function (function): The function to be executed when the menu item is selected.
        """
        self.menu_items.append(MenuItem(caption, position,function))

    def draw_menu(self, surface):
        """
        Draws the menu on the given surface.

        Args:
            surface (pygame.Surface): The surface onto which the menu will be drawn.
        """
        if not self.is_drawn:
            surface.blit(self.menu_surface, (200, 50))
            self.draw_menu_items(surface)
            pygame.display.flip()
            self.is_drawn=True
    def draw_menu_items(self, surface):
        """
        Draws each menu item on the given surface.

        Args:
            surface (pygame.Surface): The surface onto which the menu items will be drawn.
        """
        for item in self.menu_items:
            item.draw(surface)