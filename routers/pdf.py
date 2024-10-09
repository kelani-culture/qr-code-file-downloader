from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from service.auth import get_current_user
from service.token import handle_file_upload

routers = APIRouter(prefix="/doc", tags=["User File"])



@routers.post("/upload-file")
async def file_upload(
    file: Annotated[UploadFile, File(...)], user=Depends(get_current_user)
) -> JSONResponse:
    print(user) 
    url = await handle_file_upload(user.uid, file)
    return JSONResponse(content={"message": "File uploaded successfully", "url": url})

#TODO delete this route after done with test do not push to Production
@routers.get("/protected-router")
async def protected_damn(user=Depends(get_current_user)):
    return {"message":"I'm bloody protected dawg f you"}