from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from models.pdf import Document  # noqa: F401
from service.auth import get_current_user

routers = APIRouter(prefix="/file", tags=["User File"])


@routers.post("/")
async def pdf_converter(
    file: Annotated[UploadFile, File(...)], user=Depends(get_current_user)
):
    ...


#TODO delete this route after done with test do not push to Production
@routers.get("/protected-router")
async def protected_damn(user=Depends(get_current_user)):
    return {"message":"I'm bloody protected dawg f you"}