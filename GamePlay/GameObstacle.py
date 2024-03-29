from Configuration.Obstacle import Obstacle

class GameObstacle:
    def __init__(self, obstacle: Obstacle, X, Y, image):
        self.X = X
        self.Y = Y
        self.width = obstacle.width
        self.height = obstacle.height
        self.image = image