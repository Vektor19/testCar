from GamePlay import Game
from Configuration import Configuration
import argparse
from Data import RecordDb
from Data import User
import time
class App:
    """
    Represents the main application for running the game.

    Attributes:
        db (RecordDb): The database for storing game records.
        parser (argparse.ArgumentParser): The argument parser for command-line configuration.
        args (argparse.Namespace): The parsed command-line arguments.
        configuration (Configuration): The configuration object for the game.
        leaderboard (list): The leaderboard containing top records.
        game (Game): The game object.
    """
    def __init__(self):
        """
        Initializes the App object.
        """
        self.db=RecordDb()
        self.__parse_arguments()

    def start(self):
        """
        Starts the game.
        """
        self.game = Game(self.configuration, self.leaderboard)
        self.game.run()
    def load_leaderboard(self):
        """
        Loads the leaderboard from the database.
        """
        self.leaderboard = self.db.get_top_records()

    def configure(self):
        """
        Configures the game based on user input.
        """
        self.load_leaderboard()
        try:
            self.configuration = Configuration(self.args)
        except ValueError as e:
            print(e)
            exit()
    def exit(self):
        """
        Performs actions before exiting the application.
        """
        user = self.db.get_user_by_nickname(self.configuration.nickname)
        if user:
            self.db.update_record(user, max(user.record,self.game.score))
        else:
            self.db.add_record(User(self.configuration.nickname, self.game.score))
        time.sleep(5)

    def __parse_arguments(self):
        """
        Parses command-line arguments for configuring the game.
        """
        self.parser = argparse.ArgumentParser(description='Configuration game')
        self.parser.add_argument('-nick', '--nickname', type=str, help='Set user nickname', default='User')
        self.parser.add_argument('-diff', '--difficulty', type=str, help='Set difficulty level', default='easy')
        self.parser.add_argument('-car', '--car', type=str, help='Set car type ', default='bmw')
        self.parser.add_argument('-map', '--map', type=str, help='Set map type', default='winter')
        self.args = self.parser.parse_args()