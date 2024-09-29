from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from exceptions import UserAlreadyExist
from schemas.user_schemas import BadResponseSchema, SignUpResponseSchema, SignUpSchema
from service.auth import register_user

routers = APIRouter(prefix="/user")


@routers.post(
    "/signup",
    response_model=Union[SignUpResponseSchema, BadResponseSchema],
    status_code=201,
)
def user_signup(
    user: SignUpSchema, db: Session = Depends(get_db)
) -> SignUpResponseSchema | BadResponseSchema:
    """
        User signup routes
    """
    try:
        register_user(db, user.email, user.password)
    except UserAlreadyExist:
        return BadResponseSchema(
            message="User email already exists please login", status_code=400
        )

    return SignUpResponseSchema(message="User registration successful", status_code=201)
