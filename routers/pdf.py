from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from service.auth import get_current_user
from service.handle_doc import handle_file_upload

routers = APIRouter(prefix="/doc", tags=["User File"])


@routers.post("/upload-file")
async def file_upload(
    file: Annotated[UploadFile, File(...)], user=Depends(get_current_user)
) -> JSONResponse:
    url = await handle_file_upload(user.uid, file)
    return JSONResponse(
        content={
            "message": "File uploaded successfully",
            "file_url": url[0],
            "qr_code_url": url[1],
        }
    )


@routers.get("/download/{file_id}")
async def file_download(file_id: str) -> FileResponse:
    ...