from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from hashids import Hashids #type: ignore
from schemas.settings import settings
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError
from models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


setting = settings()
hashid = Hashids(salt=setting.hash_salt, min_length=10)



def verify_id_token(token: str):
    cred = HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        decode_token = auth.verify_id_token(token)
        print(decode_token)
        return decode_token
    except InvalidIdTokenError:
        raise cred










def hash_password(raw_pass: str) -> str:
    return pwd_context.hash(raw_pass)


def verify_hash_password(raw_pass: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_pass, hashed_password)


def authenticate_user(db: Session, email: str, password: str ) -> User | None:
    """
    Authenticate user with both email and password
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_hash_password(password, user.password):
        return None
    return user

def hash_id(user_id: int) -> str:
    """
    hash user id
    """
    return hashid.encode(user_id)


def un_hash_id(hashed_val: str) -> str:
    """
    decode user id
    """
    return hashid.decode(hashed_val) 