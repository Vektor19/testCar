from Configuration.Car import Car
from Configuration.Level import Level
from Configuration.Map import Map
from Configuration.Obstacle import Obstacle
import os
class Configuration:
    """
    Configuration class for setting up parameters and objects for a car racing game.

    Attributes:
        carNames (list): List of available car names based on images in the 'resources/images/cars' directory.
        mapNames (list): List of available map names based on images in the 'resources/images/maps' directory.
        levelNames (list): List of available difficulty levels: ["easy", "medium", "hard"].
        nickname (str): Player's nickname.
        obstacleNames (list): List of available obstacle names based on images in the 'resources/images/obstacles' directory.
        obstacles (list): List to store Obstacle objects.
        font_color (tuple): RGB tuple representing font color based on the selected map.

    Example usage:
        params = {'nickname': 'Player1', 'car': 'sports_car', 'map': 'city', 'difficulty': 'medium'}
        config = Configuration(params)
    """
    def __init__(self, params):
        """
            Constructor method to initialize the Configuration object.
            Args:
                params (object): Object containing user-defined parameters for the game.
        """
        self.carNames = self.get_names("resources/images/cars")
        self.mapNames = self.get_names("resources/images/maps")
        self.levelNames = ["easy", "medium", "hard"]
        self.nickname = params.nickname
        self.obstacleNames = self.get_names("resources/images/obstacles")
        self.check_errors(params)
        self.obstacles=[]
        self.configure_objects(params)
        self.font_color = self.get_color_score(params)
        
    def configure_objects(self, params):
        """
        Configures Car, Map, Level, and Obstacle objects based on user-defined parameters.

        Args:
            params (object): Object containing user-defined parameters for the game.
        """
        self.car = Car("resources/images/cars/" + str(params.car)+".png")
        self.map = Map("resources/images/maps/" + str(params.map)+".png")
        if(params.difficulty == "easy"):
            self.level = Level(params.difficulty, 1)
        elif(params.difficulty == "medium"):
            self.level = Level(params.difficulty, 1.5)
        elif(params.difficulty == "hard"):
            self.level = Level(params.difficulty, 3)
        for i in self.obstacleNames:
            self.obstacles.append(Obstacle("resources/images/obstacles/" + i + ".png"))
              
    def get_names(self, directory):
        """
        Gets the names of images (without file extension) in the specified directory.

        Args:
            directory (str): Path to the directory containing images.

        Returns:
            list: List of image names.
        """
        image_names = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith(".png"):
                    image_names.append(os.path.splitext(filename)[0])
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
        return image_names 
    
    def check_errors(self, params):
        """
        Checks for errors in user-defined parameters and raises ValueErrors if any.

        Args:
            params (object): Object containing user-defined parameters for the game.
        """
        if params.car not in self.carNames:
            raise ValueError(f"Car doesn't exist. Here is the list of cars: {', '.join(self.carNames)}")
        if params.map not in self.mapNames:
            raise ValueError(f"Map doesn't exist. Here is the list of map names: {', '.join(self.mapNames)}")
        if params.difficulty not in self.levelNames:
            raise ValueError(f"Level doesn't exist. Here is the list of levels: {', '.join(self.levelNames)}")
        
    def get_color_score(self,params):
        """
            Determines font color based on the selected map.

            Returns:
                tuple: RGB tuple representing font color.
        """
        if(params.map == "winter" or params.map == "desert"):
            return(0, 0, 0)
        if(params.map == "summer" or params.map == "spring"):
            return (255, 255, 255)


   
   
   
   
   
   
   
   
   

   