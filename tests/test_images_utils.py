import pytest
from GamePlay import ImagesUtils
from tests.game_conftest import prepare_tmp_file, unexist_path, prepare_image


class TestGame:
    def test_loading_unexist_files(self, unexist_path):        
        with pytest.raises(FileExistsError):
            _ = ImagesUtils.load_image(unexist_path)

    def test_loading_images(self, prepare_image):
        image = ImagesUtils.load_image(prepare_image)
        assert image is not None

    @pytest.mark.parametrize('prepare_tmp_file', ['txt', 'doc', 'pdf', 'mp3', 'mp4', 'exe'], indirect=True)
    def test_loading_not_images(self, prepare_tmp_file):        
        with pytest.raises(ValueError):
            _ = ImagesUtils.load_image(prepare_tmp_file)

