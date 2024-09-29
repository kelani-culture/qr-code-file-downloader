from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str

class SignUpSchema(UserSchema):
    ...

class SignUpResponseSchema(BaseModel):
    message: str
    status_code: int

class LoginSchema(UserSchema): ...


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"
    expiry_time: datetime


class BadResponseSchema(SignUpResponseSchema):
    message: str
    status_code: int