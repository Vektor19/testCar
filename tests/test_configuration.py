import pytest
from Configuration import Configuration

class Params:
    def __init__(self, nickname, difficulty, car, map):
        self.nickname = nickname
        self.difficulty = difficulty
        self.car = car
        self.map = map

class TestConfiguration:    
    @pytest.fixture
    def sample_configuration(self):
        params = Params(nickname='User', difficulty='medium', car='bmw', map='winter')
        return Configuration(params)
        
    def test_configuration_initialization(self, sample_configuration):
        assert sample_configuration.carNames == sample_configuration.get_names("resources/images/cars")
        assert sample_configuration.mapNames == sample_configuration.get_names("resources/images/maps")
        assert sample_configuration.levelNames == ["easy", "medium", "hard"]
        assert sample_configuration.nickname == 'User'
        assert sample_configuration.obstacleNames == sample_configuration.get_names("resources/images/obstacles")

    def test_check_errors_success(self, sample_configuration):
        assert sample_configuration

    @pytest.mark.parametrize("nickname, difficulty, car, map, expected_error", [
        ('User', 'medium', 'bmw', 'ggmap', ValueError),
        ('User', 'medium', 'carexit', 'winter', ValueError),
        ('User', 'nonelvl', 'bmw', 'winter', ValueError),
    ])
    def test_check_errors_failed(self, nickname, difficulty, car, map, expected_error):
        params = Params(nickname=nickname, difficulty=difficulty, car=car, map=map)
        with pytest.raises(expected_error):
            Configuration(params)

    @pytest.mark.parametrize("directory", [
        "resources/images/cars",
        "resources/images/maps",
        "resources/images/obstacles",
    ])
    def test_get_names_exist_directory(self, sample_configuration, directory):
        assert sample_configuration.get_names(directory)  # Перевіряємо, що повертається список імен
        
    def test_get_names_nonexistent_directory(self, sample_configuration, tmp_path):
        try:
            sample_configuration.get_names("nonexistent_directory")
        except FileNotFoundError:
            pytest.fail("Expected FileNotFoundError, but no exception was raised.")

