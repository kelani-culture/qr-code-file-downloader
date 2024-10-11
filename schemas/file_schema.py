from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel



class UserFileResponse(BaseModel):
    message: str
    file_url: Optional[str]
    qrcode_url: str
    qr_code_img_url: str




class FileUploadOrUrl(BaseModel):
    file: Optional[UploadFile] = None
    url: Optional[str] = None