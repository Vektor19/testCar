from pymongo import MongoClient

class RecordDb:
    """
    The RecordDb class is designed to work with a MongoDB database where user records are stored.

    Constructor parameters:
        db_name (str): The name of the MongoDB database. Default is 'user_record'.

    Class attributes:
        client: MongoClient: MongoDB client for connecting to the database server.
        db: Database: Reference to the MongoDB database.
        records_collection: Collection: The 'records' collection in the database where user records are stored.

    Methods:
        update_user(old_nickname, new_nickname): Updates the user's nickname in the database.
        delete_user(user): Deletes a user from the database.
        add_record(user): Adds a new user record to the database.
        get_top_records(limit=3): Returns the top N user records in descending order of their records.
        update_record(user, new_record): Updates a user record with a new record.
        get_user_by_nickname(nickname): Retrieves a user from the database by their nickname.
    """

    def __init__(self, db_name='user_record'):
        """
        Initializes an instance of the RecordDb class.

        Parameters:
            db_name (str): The name of the MongoDB database. Default is 'user_record'.
        """
        self.client = MongoClient('mongodb+srv://vektor19:0957422713@cluster1.xk6ovkq.mongodb.net/')
        self.db = self.client[db_name]
        self.records_collection = self.db['records']

    def update_user(self, old_nickname, new_nickname):
        """
        Updates the user's nickname in the database.

        Parameters:
            old_nickname (str): The old nickname of the user.
            new_nickname (str): The new nickname of the user.
        """
        self.records_collection.update_many({'nickname': old_nickname}, {'$set': {'nickname': new_nickname}})

    def delete_user(self, user):
        """
        Deletes a user from the database.

        Parameters:
            user (User): The user object to be deleted.
        """
        self.records_collection.delete_many({'nickname': user.nickname})

    def add_record(self, user):
        """
        Adds a new user record to the database.

        Parameters:
            user (User): The user object for which to add a record.
        """
        record_data = {'nickname': user.nickname, 'record': user.record}
        self.records_collection.insert_one(record_data)

    def get_top_records(self, limit=3):
        """
        Returns the top N user records in descending order of their records.

        Parameters:
            limit (int): The number of records to return. Default is 3.

        Returns:
            list: List of user objects with top records.
        """
        top_records = self.records_collection.find().sort('record', -1).limit(limit)
        return [User(record['nickname'], record['record']) for record in top_records]

    def update_record(self, user, new_record):
        """
        Updates a user record with a new record.

        Parameters:
            user (User): The user object whose record needs to be updated.
            new_record (int): The new record of the user.
        """
        self.records_collection.update_one({'nickname': user.nickname}, {'$set': {'record': new_record}})

    def get_user_by_nickname(self, nickname):
        """
        Retrieves a user from the database by their nickname.

        Parameters:
            nickname (str): The nickname of the user.

        Returns:
            User or None: The user object if found by nickname, or None if no user with such nickname is found.
        """
        user_data = self.records_collection.find_one({'nickname': nickname})
        if user_data:
            return User(user_data['nickname'], user_data['record'])
        else:
            return None


class User:
    """
    The User class represents a user with their nickname and record.

    Constructor parameters:
        nickname (str): The nickname of the user.
        record (int): The record of the user. Default is 0.
    """

    def __init__(self, nickname, record=0):
        """
        Initializes an instance of the User class with the specified nickname and record.

        Parameters:
            nickname (str): The nickname of the user.
            record (int): The record of the user. Default is 0.
        """
        self.nickname = nickname
        self.record = record
