import io

from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from firebase_admin import storage

from schemas.file_schema import UserFileResponse
from service.auth import get_current_user
from service.handle_doc import (
    handle_file_upload,
    handle_user_qrcode_download,
    user_file,
)

routers = APIRouter(prefix="/doc", tags=["User File"])


@routers.post("/upload-file-or-url")
async def file_upload(
    file: UploadFile = File(None),
    url: str = Form(None),
    user=Depends(get_current_user),
) -> UserFileResponse:
    if not url.startswith("https://"):
        return JSONResponse(
            content={"message": "Invalid URL resource provided"}, status_code=400
        )

    url = await handle_file_upload(user.uid, file, url)
    return UserFileResponse(
        message="File uploaded successfully", file_url=url[0], qrcode_url=url[1], qr_code_img_url=url[2]
    )


@routers.get("/download/file/{file_id}")
async def file_download(
    file_id: str, user=Depends(get_current_user)
) -> StreamingResponse:
    """
    download user file
    """
    # local_path = "./tmp/download"
    file = await user_file(file_id)
    u_file = file.to_dict()
    bucket = storage.bucket()
    blob = bucket.blob(u_file.get("file_path"))

    file_content = blob.download_as_bytes()
    file_stream = io.BytesIO(file_content)

    return StreamingResponse(
        file_stream,
        media_type="application/octet-stream",
        # filename=file.get("file_name"),
        headers={
            "Content-Disposition": f'attachment; filename="{u_file.get("file_name")}"'
        },
    )


@routers.get("/download/qrcode/{qrcode_id}")
async def qrcode_download(
    qrcode_id: str, user=Depends(get_current_user)
) -> StreamingResponse:
    """
    route user qrcode...
    """
    qrcode = await handle_user_qrcode_download(qrcode_id)

    bucket = storage.bucket()
    u_qrcode = qrcode.to_dict()
    blob = bucket.blob(u_qrcode.get("qr_path"))
    qr_content = blob.download_as_bytes()
    qr_stream = io.BytesIO(qr_content)
    return StreamingResponse(
        qr_stream,
        media_type="application/octet-stream",
        # filename=file.get("file_name"),
        headers={
            "Content-Disposition": f'attachment; filename="qrcode_{u_qrcode.get("id")}"'
        },
    )
