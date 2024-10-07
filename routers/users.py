from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from exceptions import InvalidEmailOrPassword, UserAlreadyExist
from schemas.user_schemas import (
    BadResponseSchema,
    LoginResponseSchema,
    LoginSchema,
    SignUpResponseSchema,
    SignUpSchema,
)
from service.auth import register_user, user_login

routers = APIRouter(prefix="/auth/user")


@routers.post(
    "/signup",
    response_model=Union[SignUpResponseSchema, BadResponseSchema],
    status_code=201,
)
async def user_signup(
    user: SignUpSchema, db: Session = Depends(get_db)
) -> SignUpResponseSchema | JSONResponse:
    """
    User signup routes
    """
    try:
       await register_user(db, user.email, user.password)
    except UserAlreadyExist:
        bad_resp = BadResponseSchema(
            message="User email already exists please login", status_code=400
        ).model_dump()
        return JSONResponse(content=bad_resp, status_code=400)

    return SignUpResponseSchema(message="User registration successful", status_code=201)


@routers.post("/login", response_model=Union[LoginResponseSchema, BadResponseSchema])
async def login_user(
    data: LoginSchema, db: Session = Depends(get_db)
) -> LoginResponseSchema | JSONResponse:
    """
    login route
    """
    try:
        user = await user_login(db, data.email, data.password)
    except InvalidEmailOrPassword:
        bad_resp = BadResponseSchema(
            message="Invalid email or password provided", status_code=400
        ).model_dump()
        return JSONResponse(content=bad_resp, status_code=400)

    return LoginResponseSchema(**user)# type: ignore
