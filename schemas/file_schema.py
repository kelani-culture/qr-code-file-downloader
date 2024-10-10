from pydantic import BaseModel



class FileResponse(BaseModel):
    download_url: str
    qrcode_img: str