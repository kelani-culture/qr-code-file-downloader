import pytest
from faker import Faker
from sqlalchemy.orm import Session

from exceptions import UserAlreadyExist
from models.users import User
from service.auth import register_user

fake = Faker()


def test_register_user_success(mocker, db_session: Session):
    # Arrange
    email = fake.email()
    password = fake.password()
    hashed_password = "$2b$12$4YUIjWNhY3bKICJsP0n0PePP5.x8aCw7Tvj9qlupjW0FrMoRLa1Iq"

    # Mock the hash_password function
    # utils.hash_password = lambda x: hashed_password
    mock_hash = mocker.patch("service.auth.hash_password", return_value=hashed_password)

    register_user(db_session, email, password)

    # Assert
    mock_hash.assert_called_once_with(password)
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.email == email
    assert user.password == hashed_password


def test_register_user_already_exists(db_session: Session):
    email = fake.email()
    password = fake.password()
    existing_user = User(email=email, password="existing_password")
    db_session.add(existing_user)
    db_session.commit()

    # Act & Assert
    with pytest.raises(UserAlreadyExist):
        register_user(db_session, email, password)

def test_register_user_password_hashing(db_session: Session, mocker):
    # Arrange
    email = fake.email()
    password = fake.password()
    mock_hash = mocker.patch("service.auth.hash_password", return_value="mocked_hash")
    
    # Act
    register_user(db_session, email, password)
    
    # Assert
    mock_hash.assert_called_once_with(password)
    user = db_session.query(User).filter(User.email == email).first()
    assert user is not None
    assert user.password == "mocked_hash"