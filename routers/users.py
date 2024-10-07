from typing import Annotated, Union

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from exceptions import InvalidEmailOrPassword, UserAlreadyExist
from schemas.user_schemas import (
    BadResponseSchema,
    GoogleSignInToken,
    LoginResponseSchema,
    RefreshToken,
    SignUpResponseSchema,
    SignUpSchema,
)
from service.auth import google_auth, register_user, user_login, generate_new_id_token

routers = APIRouter(prefix="/auth/user", tags=["Auth"])


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
    data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> LoginResponseSchema | JSONResponse:
    """
    login route
    """
    try:
        user = await user_login(db, data.username, data.password)
    except InvalidEmailOrPassword:
        bad_resp = BadResponseSchema(
            message="Invalid email or password provided", status_code=400
        ).model_dump()
        return JSONResponse(content=bad_resp, status_code=400)

    return LoginResponseSchema(**user)  # type: ignore


@routers.post("/google-sign-in")
async def goolge_auth_sign_up(google_token: GoogleSignInToken) -> JSONResponse:
    res = google_auth(google_token.token)
    return JSONResponse(content=res, status_code=res["status_code"])



@routers.post("/refresh-token")
async def refresh_token(request: Request, r_token: Annotated[RefreshToken, Header()]) -> JSONResponse:
    """
    user refresh token
    """
    token = await generate_new_id_token(r_token.refresh_token)
    return JSONResponse(content=token, status_code=200)