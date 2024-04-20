import uuid
from typing import Annotated, Literal

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query

from api.auth.auth_repository import AuthRepository
from api.chemas.SImages import SImageAdd
from api.chemas.SUser import SUser
from api.repositories.images_repository import ImagesRepository

router = APIRouter(
    prefix="/your_train",
    tags=['Images']
)
IMAGEDIR = "api/images/"


@router.post('/images_upload/')
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
        raise HTTPException(status_code=500, detail="Error uploading image")

