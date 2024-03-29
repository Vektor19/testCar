from Configuration.Car import Car


class GameCar:
    def __init__(self, car: Car, X, Y, velocity):
        self.X = X
        self.Y = Y
        self.width = car.width
        self.height = car.height
        self.velocity = velocity