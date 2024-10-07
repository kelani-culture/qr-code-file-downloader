import json
from typing import Annotated, Dict, Union

from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from fastapi import Depends, HTTPException
from firebase_admin import auth
from firebase_admin.auth import EmailAlreadyExistsError, InvalidIdTokenError
from firebase_admin.exceptions import FirebaseError
from google.auth.transport import requests
from google.oauth2 import id_token
from httpx import HTTPError
from sqlalchemy.orm import Session

from exceptions import InvalidEmailOrPassword, InvalidTokenProvided, UserAlreadyExist
from schemas.settings import settings

setting = settings()  # jwt token settings



oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="/user/auth/login"
)

async def register_user(db: Session, email: str, password: str) -> None:
    """
    Handles users registration....
    """
    try:
        auth.create_user(
            email=email,
            password=password,
            email_verified=False,
        )
    except EmailAlreadyExistsError:
        raise UserAlreadyExist()
    except FirebaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    auth.generate_email_verification_link(email=email, action_code_settings=None)


async def user_login(db: Session, email: str, password: str) -> Dict[str, str]:
    """
    handles user login
    """
    FIREBASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    try:
        async with httpx.AsyncClient() as client:
            payload = json.dumps(
                {"email": email, "password": password, "returnSecureToken": True}
            )
            resp = await client.post(
                f"{FIREBASE_URL}?key={setting.web_api_key}", data=payload
            )
            resp.raise_for_status()

            data = {
                "email": resp.json()["email"],
                "id_token": resp.json()["idToken"],
                "refresh_token": resp.json()["refreshToken"],
                "expires_in": resp.json()["expiresIn"],
            }
            return data
    except HTTPError:
        raise InvalidEmailOrPassword()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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


def google_auth(token: str) -> Dict[str, Union[str, int]]:
    WEB_CLIENT_ID: str = setting.web_client_id
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), WEB_CLIENT_ID)
        # Google Sign In specific check
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise InvalidTokenProvided("Wrong Issuer provided")

        # userid = idinfo["sub"]
        email = idinfo["email"]
        try:
            auth.get_user_by_email(email)
            return {"message": "User already_exists", "status_code": 400}
        except auth.UserNotFoundError:
            auth.create_user(email=email, email_verified=idinfo["email_verified"])
    except InvalidTokenProvided:
        return {"message": "Invalid token provided", "status_code": 400}

    return {"message": "User email already exists", "status_code": 201}
