import pytest
from unittest.mock import MagicMock
from Data.RecordDb import RecordDb, User

@pytest.fixture
def mock_db():
    # Create a mock MongoClient and database
    mock_db = MagicMock()
    mock_client = MagicMock()
    mock_client.__getitem__.return_value = mock_db
    record_db = RecordDb()
    record_db.client = mock_client
    return record_db

def test_update_user(mock_db):
    # Mock the update_many method
    mock_db.records_collection.update_many = MagicMock()
    # Call the method
    mock_db.update_user('old_nickname', 'new_nickname')
    # Check if update_many was called with correct arguments
    mock_db.records_collection.update_many.assert_called_once_with({'nickname': 'old_nickname'}, {'$set': {'nickname': 'new_nickname'}})

def test_delete_user(mock_db):
    # Mock the delete_many method
    mock_db.records_collection.delete_many = MagicMock()
    # Create a dummy user
    user = User('test_user')
    # Call the method
    mock_db.delete_user(user)
    # Check if delete_many was called with correct arguments
    mock_db.records_collection.delete_many.assert_called_once_with({'nickname': 'test_user'})

def test_add_record(mock_db):
    # Mock the insert_one method
    mock_db.records_collection.insert_one = MagicMock()
    # Create a dummy user
    user = User('test_user', 10)
    # Call the method
    mock_db.add_record(user)
    # Check if insert_one was called with correct arguments
    mock_db.records_collection.insert_one.assert_called_once_with({'nickname': 'test_user', 'record': 10})

def test_get_top_records(mock_db):
    # Mock the find and sort methods
    mock_db.records_collection.find = MagicMock(return_value=MagicMock())
    mock_db.records_collection.find().sort = MagicMock(return_value=MagicMock())
    # Call the method
    top_records = mock_db.get_top_records(3)
    # Check if find and sort methods were called with correct arguments
    mock_db.records_collection.find().sort.assert_called_once_with('record', -1)
    # Assuming you have User objects in the database, check if User objects are returned
    assert all(isinstance(user, User) for user in top_records)

def test_update_record(mock_db):
    # Mock the update_one method
    mock_db.records_collection.update_one = MagicMock()
    # Create a dummy user
    user = User('test_user', 10)
    # Call the method
    mock_db.update_record(user, 20)
    # Check if update_one was called with correct arguments
    mock_db.records_collection.update_one.assert_called_once_with({'nickname': 'test_user'}, {'$set': {'record': 20}})

def test_get_user_by_nickname(mock_db):
    # Mock the find_one method
    mock_db.records_collection.find_one = MagicMock(return_value={'nickname': 'test_user', 'record': 10})
    # Call the method
    user = mock_db.get_user_by_nickname('test_user')
    # Check if find_one was called with correct arguments
    mock_db.records_collection.find_one.assert_called_once_with({'nickname': 'test_user'})
    # Check if User object is returned
    assert isinstance(user, User)
    assert user.nickname == 'test_user'
    assert user.record == 10

if __name__ == "__main__":
    pytest.main()
