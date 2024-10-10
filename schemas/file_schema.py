from pydantic import BaseModel



class UserFileResponse(BaseModel):
    message: str
    file_url: str
    qrcode_url: str