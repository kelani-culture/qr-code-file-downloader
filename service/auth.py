from sqlalchemy.orm import Session
from exceptions import UserAlreadyExist
from models.users import User

from .utils import hash_password


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
