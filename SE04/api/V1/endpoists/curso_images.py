import shutil
import os
from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi.responses import HTMLResponse, FileResponse # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession # type: ignore
from fastapi import File, UploadFile

router = APIRouter()

@router.get('/', status_code=status.HTTP_202_ACCEPTED)
async def get_cursos():
    return "endpoint da imagem"


UPLOAD_DIRECTORY = "../uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload-image/")
async def create_upload_file(upload_file: UploadFile = File(...)): 
    content =  upload_file.filename
    file_location = f"{UPLOAD_DIRECTORY}/{upload_file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {"filename": content}

@router.get("/images/{filename}")
async def get_image(filename: str):
    file_location = f"{UPLOAD_DIRECTORY}/{filename}"
    if os.path.exists(file_location):
        return FileResponse(file_location)
    raise HTTPException(status_code=404, detail="Image not found")