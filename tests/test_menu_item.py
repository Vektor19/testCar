from unittest.mock import MagicMock

import pygame
import pytest
from GamePlay.MenuItem import MenuItem


class TestMenuItem:
    def temp_func(self):
        return

    @pytest.fixture
    def menu_item(self):
        pygame.init()
        menu_item = MenuItem('Exit', (100, 400), self.temp_func, (300, 140))
        return menu_item

    @pytest.mark.parametrize('caption,position,function,size', [('Continue', (100, 100), temp_func, (300, 100)),
                                                                ('Restart', (100, 250), temp_func, (300, 100)),
                                                                ('Exit', (100, 400), temp_func, (300, 140))])
    def test_menu_item_initialization(self, caption, position, function, size):
        # Define test caption, position, and function

        # Create a MenuItem object
        menu_item = MenuItem(caption, position, function, size)

        # Test attributes initialization
        assert menu_item.caption == caption
        assert menu_item.position == position
        assert menu_item.rect.topleft == position
        assert menu_item.rect.size == size
        assert isinstance(menu_item.font, pygame.font.Font)
        assert isinstance(menu_item.img, pygame.Surface)
        assert menu_item.function == function

    def test_is_clicked(self, menu_item):
        """Test is_clicked method of MenuItem."""
        assert menu_item.is_clicked((150, 450)) == True
        assert menu_item.is_clicked((100, 400)) == True
        assert menu_item.is_clicked((50, 50)) == False
