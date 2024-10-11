import json
from typing import Annotated, Dict, Optional

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from firebase_admin import auth
from firebase_admin.auth import EmailAlreadyExistsError, InvalidIdTokenError
from firebase_admin.exceptions import FirebaseError
from google.auth.transport import requests
from google.oauth2 import id_token
from httpx import HTTPError
from sqlalchemy.orm import Session

from exceptions import InvalidEmailOrPassword, UserAlreadyExist
from schemas.settings import settings

setting = settings()  # jwt token settings


oauth2_password_scheme = HTTPBearer()


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
    FIREBASE_URL = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    )
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
                "access_token": resp.json()["idToken"],
                "refresh_token": resp.json()["refreshToken"],
                "expires_in": resp.json()["expiresIn"],
            }
            return data
    except HTTPError:
        raise InvalidEmailOrPassword()


def get_current_user(
    request: Request, token: Annotated[Optional[str], Depends(oauth2_password_scheme)]
):
    """get current user login info"""
    cred = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.headers.get("Authorization")
        if not token or "Bearer" not in token:
            raise cred

        token = token.split(" ")[1]
        decode_token = auth.verify_id_token(token)

        user = auth.get_user(decode_token.get("uid"))
        return user
    except InvalidIdTokenError:
        raise cred


async def google_auth(id_token_str: str) -> Dict[str, str]:
    """Authenticate user with Google ID token."""
    WEB_CLIENT_ID: str = setting.web_client_id
    try:
        # Verify the ID token
        idinfo = id_token.verify_oauth2_token(
            id_token_str, requests.Request(), WEB_CLIENT_ID
        )

        # Check issuer
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise ValueError("Wrong issuer.")

        # Get or create the user in Firebase
        email = idinfo["email"]
        try:
            user = auth.get_user_by_email(email)
            message = "Login successful"
        except auth.UserNotFoundError:
            user = auth.create_user(
                email=email, email_verified=idinfo["email_verified"]
            )
            message = "User created successfully"

        # Create a custom token
        custom_token = auth.create_custom_token(user.uid)  # No need for decode here

        return {
            "message": message,
            "firebase_token": custom_token,  # Send it directly
        }

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid token: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}",
        )


async def generate_new_id_token(token: str) -> Dict[str, str]:
    """
    generate new id token for the user from firebase
    """
    firebase_url = "https://securetoken.googleapis.com/v1/token?key={}".format(
        setting.web_api_key
    )
    try:
        async with httpx.AsyncClient() as client:
            payloads = {"refresh_token": token, "grant_type": "refresh_token"}
            pay_json = json.dumps(payloads)
            resp = await client.post(firebase_url, data=pay_json)

            resp.raise_for_status()
        data: Dict[str, str] = resp.json()
        data.pop("access_token")
        data.pop("project_id")
        return data
    except HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))
