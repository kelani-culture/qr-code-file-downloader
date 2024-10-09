import uuid

from fastapi import HTTPException, UploadFile
from firebase_admin import firestore, storage

import fire  # noqa

db = firestore.client()


FILE_EXTENSION = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".svg",
    ".webp",
    ".heic",
    ".ico",
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".m4a",
    ".aiff",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".flv",
    ".wmv",
    ".webm",
    ".3gp",
    ".pdf",
    ".doc",
    ".xls",
    ".ppt",
    ".pptx",
    ".txt",
    ".rt",
    ".odt",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".iso",
    ".exe",
    ".bat",
    ".sh",
    ".app",
    ".msi",
    ".html",
    ".css",
    ".js",
    ".php",
    ".xml",
    ".json",
    ".sql",
    ".asp",
    ".epub",
    ".mobi",
    ".psd",
    ".ai",
}


async def handle_file_upload(user_id: str, file: UploadFile) -> str:
    """
    Handle user file upload to firestore
    """
    # user_ref = db.collection("users").document(user_id)
    # user_data = user_ref.get()
    # if not user_data.exists:
    #     raise HTTPException(status_code=404, detail="User not found")
    file_url = ""
    try:
        file_ext = file.filename.split(".")[1]

        if "."+file_ext not in FILE_EXTENSION:
            raise HTTPException(status_code=400, detail="File not supported")
        unique_filename = f"{file.filename}{uuid.uuid4()}.{file_ext}"

        file_path = f"user_file/{user_id}/{unique_filename}"
        # upload file to firebase storage
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file, content_type=file.content_type)

        # make file publicly accessible
        blob.make_public()
        file_url = blob.public_url

        file_data = {
            "user_id": user_id,
            "file_name": file.filename,
            "unique_filename": unique_filename,
            "file_path": file_path,
            "file_ext": file_ext,
            "file_public_url": file_url,
            "content_type": file.content_type,
            "uploaded_at": firestore.SERVER_TIMESTAMP,
        }
        db.collection("user_file").add(file_data)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    return file_url


def create_qr_code(file_url: str): ...


# this are being commenterd because ion know But I won't push this to production of cause...
# from datetime import datetime, timedelta
# from typing import Dict, Union

# import jwt
# from fastapi import HTTPException, status
# from jwt.exceptions import InvalidTokenError
# from sqlalchemy.orm import Session

# from models.users import User

# ALGORITHM = "HS256"


# def create_jwt_token(
#     data: Dict[str, Union[str, datetime]], secret_key: str, expired_min: timedelta
# ) -> str:
#     """
#     function for creating both refresh token and access token for the user authorization
#     """
#     expires = datetime.now() + expired_min
#     data["exp"] = expires
#     return jwt.encode(payload=data, key=secret_key, algorithm=ALGORITHM)


# def decode_jwt_token(db: Session, token: str, secret_key: str) -> User:
#     """
#     decode the jwt token provided
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, key=secret_key, algorithms=[ALGORITHM])
#         user_id: int = payload.get("sub")
#         if not user_id:
#             raise credentials_exception
#     except InvalidTokenError:
#         raise credentials_exception

#     user = db.query(User).filter(User.id == user_id).first()

#     if not user:
#         raise credentials_exception
#     return user
