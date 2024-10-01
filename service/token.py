from datetime import datetime, timedelta
from typing import Dict, Union

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from models.users import User

ALGORITHM = "HS256"


def create_jwt_token(
    data: Dict[str, Union[str, datetime]], secret_key: str, expired_min: timedelta
) -> str:
    """
    function for creating both refresh token and access token for the user authorization
    """
    expires = datetime.now() + expired_min
    data["exp"] = expires
    return jwt.encode(payload=data, key=secret_key, algorithm=ALGORITHM)


def decode_jwt_token(db: Session, token: str, secret_key: str) -> User:
    """
    decode the jwt token provided
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=secret_key, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise credentials_exception
    return user
