import uuid
from io import BytesIO

import qrcode
from fastapi import HTTPException, UploadFile
from firebase_admin import firestore, storage

import fire  # noqa
from schemas.settings import settings

db = firestore.client()

setting = settings()
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
    ".docx",
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
    file_url = ""
    try:
        file_ext = file.filename.split(".")[1]

        if "." + file_ext not in FILE_EXTENSION:
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
        file_col = db.collection("user_file").add(file_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    download_url = f"{setting.backend_host}/doc/download/file/{file_col[1].id}"
    qrcode_url = await create_qr_code(file.filename, download_url, user_id, file_col) 
    return download_url, qrcode_url


async def create_qr_code(file_name: str, file_url: str, user_id: str, file_obj) -> str:
    """
    create qrcode for downloading user file
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(file_url)

    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    qr_code_path = f"qrcode/{file_name}_qrcode.png"

    # Convert image to bytes for Firebase storage
    img_bytes_array = BytesIO()
    img.save(img_bytes_array, format="PNG")
    img_bytes_array.seek(0)

    bucket = storage.bucket()
    blob = bucket.blob(qr_code_path)
    blob.upload_from_file(img_bytes_array, content_type="image/png")

    # Make the file publicly accessible and get the URL
    blob.make_public()
    qr_code_url = blob.public_url

    data = {
        "qr_path": qr_code_path,
        "qrcode_url": qr_code_url,
        "file_id": file_obj[1].id,
        "user_id": user_id,
    }

    qr_col = db.collection("qrcode").add(data)

    download_qr = f"{setting.backend_host}/doc/download/qrcode/{qr_col[1].id}"
    return download_qr


async def user_file(file_id: str):
    """
    handle user file download
    """
    file = db.collection("user_file").document(file_id)

    file = file.get()

    if not file.exists:
        raise HTTPException(detail="File not found", status_code=404)

    return file



async def handle_user_qrcode_download(qrcode_id: str):
    """
    handle user qrcode download
    """
    qrcode = db.collection("qrcode").document(qrcode_id)
    qrcode = qrcode.get()
    if not qrcode.exists:
        raise HTTPException(status_code=404, detail="qrcode not found")
    
    return qrcode

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
