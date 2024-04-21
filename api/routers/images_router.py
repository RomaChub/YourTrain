import os
import uuid
from typing import Annotated, Literal

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from api.auth.auth_repository import AuthRepository
from api.chemas.SImages import SImageAdd, SImage
from api.chemas.SUser import SUser
from api.repositories.images_repository import ImagesRepository

router = APIRouter(
    prefix="/your_train",
    tags=['Images']
)
IMAGEDIR = "api/images/"


@router.post('/images/upload/')
async def images_upload(
        file: UploadFile = File(...),
        tag: str = Query("etc", enum=["exercise", "training", "etc"]),
        user: SUser = Depends(AuthRepository.get_current_active_auth_user)):
    try:
        file.filename = f"{uuid.uuid4()}.jpg"
        content = await file.read()

        image_data = {
            "image_path": file.filename,
            "user_id": user.id,
            "tag": tag
        }
        image_data = SImageAdd(**image_data)
        image_id = await ImagesRepository.add_one(image_data)
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(content)

        return {"filename": file.filename, "id": image_id}
    except Exception as e:
        raise HTTPException(status_code=422, detail="Error uploading image")


@router.get('/images/')
async def get_one_image(image_id: int):
    files = os.listdir(IMAGEDIR)
    images = await ImagesRepository.get_all()
    image = f"{IMAGEDIR}{images[image_id].image_path}"
    return FileResponse(image)


@router.get('/images/all/')
async def get_all_images():
    images = await ImagesRepository.get_all()
    return images
