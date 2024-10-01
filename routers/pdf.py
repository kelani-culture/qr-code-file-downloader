from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from models.pdf import Document #noqa: F401

file_converter = APIRouter()


@file_converter.post("/pdfconverter/")
async def pdf_converter(file: Annotated[UploadFile, File(...)]): ...
