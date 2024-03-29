import pygame
import pytest
from Configuration.Obstacle import Obstacle
from GamePlay import Game
from Configuration import Configuration
from tests.game_conftest import prepare_image, prepare_text_file, unexist_path

class Params:
    def __init__(self, nickname, difficulty, car, map):
        self.nickname = nickname
        self.difficulty = difficulty
        self.car = car
        self.map = map

class TestGame:
    @pytest.fixture
    def sample_configuration(self):
        params = Params(nickname='User', difficulty='medium', car='bmw', map='winter')
        return Configuration(params)

    def test_game_initialization(self, sample_configuration):
        leaders = []  # fill with some sample leader objects if needed
        game = Game(sample_configuration, leaders)
        assert game is not None
        assert game.menu is not None
        assert game.car_image is not None
        assert game.road is not None

    def get_configuration_for_loading_images(self, sample_configuration, prepare_image, unexist_file, car_image_exist, map_image_exist, obstacle_images_exist):
        configuration = sample_configuration
        if car_image_exist:
            configuration.car.photo = prepare_image
        else: configuration.car.photo = unexist_file
        
        if map_image_exist:
            configuration.map.photo = prepare_image
        else: configuration.map.photo = unexist_file
        
        configuration.obstacles = []
        for obstacle_exist in obstacle_images_exist:
            if obstacle_exist:
                configuration.obstacles.append(Obstacle(prepare_image))
            else: configuration.obstacles.append(Obstacle(unexist_file))
        
        return configuration
    
    @pytest.mark.parametrize(('car_image_exist', 'map_image_exist', 'obstacle_images_exist'), [(False, True, [True, True]),
                                                                                               (True, False, [True, True]),
                                                                                               (True, True, [False, True]),
                                                                                               (True, True, [True, False]),
                                                                                               (True, True, [False, False])])
    def test_loading_unexist_images(self, sample_configuration, prepare_image, unexist_path, car_image_exist, map_image_exist, obstacle_images_exist):
        configuration = self.get_configuration_for_loading_images(sample_configuration, prepare_image, unexist_path, car_image_exist, map_image_exist, obstacle_images_exist)
        
        with pytest.raises(FileExistsError):
            _ = Game(configuration, [])

    def test_succesful_loading_images(self, sample_configuration, prepare_image, unexist_path):
        configuration = self.get_configuration_for_loading_images(sample_configuration, prepare_image, unexist_path, True, True, [True, True, True])
        game = Game(configuration, [])
        assert game is not None

    @pytest.mark.parametrize(('car_image_exist', 'map_image_exist', 'obstacle_images_exist'), [(False, True, [True, True]),
                                                                                               (True, False, [True, True]),
                                                                                               (True, True, [False, True]),
                                                                                               (True, True, [True, False]),
                                                                                               (True, True, [False, False])])
    def test_loading_incorrect_images(self, sample_configuration, prepare_text_file, prepare_image, car_image_exist, map_image_exist, obstacle_images_exist):
        configuration = self.get_configuration_for_loading_images(sample_configuration, prepare_image, prepare_text_file, car_image_exist, map_image_exist, obstacle_images_exist)
        with pytest.raises(ValueError):
            _ = Game(configuration, [])

    def test_update_left_key_pressed(game, monkeypatch, sample_configuration):
        keys_pressed = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
        monkeypatch.setattr(pygame.key, 'get_pressed', lambda: keys_pressed)
        game = Game(sample_configuration, [])
        initial_car_x = game.car.X
        game.update()
        assert game.car.X == initial_car_x - game.car.velocity

    def test_update_right_key_pressed(game, monkeypatch, sample_configuration):
        keys_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
        monkeypatch.setattr(pygame.key, 'get_pressed', lambda: keys_pressed)
        game = Game(sample_configuration, [])
        initial_car_x = game.car.X
        game.update()
        assert game.car.X == initial_car_x + game.car.velocity