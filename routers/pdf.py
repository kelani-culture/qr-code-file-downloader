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