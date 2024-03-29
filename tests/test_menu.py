from unittest.mock import MagicMock

import pygame
import pytest
from GamePlay.MenuItem import MenuItem
from GamePlay.Menu import Menu

class TestMenu:
    def mock_resume_game(self):
        pass

    def mock_restart_game(self):
        pass

    def mock_quit_game(self):
        pass

    @pytest.fixture
    def prepared_menu(self):
        menu = Menu(self.mock_resume_game, self.mock_restart_game, self.mock_quit_game)
        return menu

    # Test the initialization of the Menu class
    def test_menu_initialization(self):
        menu = Menu(self.mock_resume_game, self.mock_restart_game, self.mock_quit_game)
        assert len(menu.menu_items) == 3
        assert menu.menu_surface.get_size() == (400, 500)
        assert menu.is_drawn == False

    # Test adding menu items
    def test_add_menu_item(self, prepared_menu):

        prepared_menu.add_menu_item("Test Item", (100, 100), self.mock_resume_game)
        assert len(prepared_menu.menu_items) == 4

    # Test drawing menu
    def test_draw_menu(self, prepared_menu):
        prepared_menu.draw_menu(pygame.Surface((800,600)))
        assert prepared_menu.is_drawn == True