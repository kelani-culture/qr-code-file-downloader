import json
from typing import Dict

import httpx
from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin.exceptions import FirebaseError
from httpx import HTTPError
from sqlalchemy.orm import Session

from exceptions import InvalidEmailOrPassword, UserAlreadyExist
from schemas.settings import settings

setting = settings()  # jwt token settings

FIREBASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


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


async def user_login(
    db: Session, email: str, password: str, **kwargs
) -> Dict[str, str]:
    """
    handles user login
    """
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
                "expires_in": resp.json()["expiresIn"]
            }
            return data
    except HTTPError:
        raise InvalidEmailOrPassword()
    except auth.InvalidIdTokenError:
        raise
