from datetime import timedelta
from typing import Dict, Union

from sqlalchemy.orm import Session

from exceptions import InvalidEmailOrPassword, UserAlreadyExist
from models.users import User
from schemas.settings import settings

from .token import create_jwt_token
from .utils import authenticate_user, hash_id, hash_password

setting = settings()  # jwt token settings


def register_user(db: Session, email: str, password: str) -> None:
    """
    Handles users registration....
    """
    user_exist = db.query(User).filter(User.email == email).first()

    if user_exist:
        raise UserAlreadyExist()
    password = hash_password(password)
    user = User(email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)


def user_login(
    db: Session, email: str, password: str, **kwargs
) -> Dict[str, Union[str, timedelta]]:
    """
    handles user login
    """
    user = authenticate_user(db, email, password)
    if user is None:
        raise InvalidEmailOrPassword()

    a_data = {"sub": hash_id(user.id), "type": "user"}  # access_token payload

    access_token = create_jwt_token(
        a_data, setting.access_token_secret_key, setting.access_token_expires_min # type: ignore
    )

    refresh_token = create_jwt_token(
        a_data, setting.refresh_token_secret_key, setting.refresh_token_expires_min #type: ignore
    )

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in_min": setting.access_token_expires_min.total_seconds() // 60,
    }
    return tokens
