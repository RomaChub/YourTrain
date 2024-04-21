from typing import List

from api.chemas.SImages import SImageAdd, SImage
from api.database.database import new_session, ExerciseOrm

from sqlalchemy import select, delete

from api.database.database import ImageOrm


class ImagesRepository:
    @classmethod
    async def add_one(cls, data: SImageAdd) -> int:
        async with new_session() as session:
            image_dict = data.model_dump()
            image = ImageOrm(**image_dict)
            session.add(image)
            await session.flush()
            await session.commit()
            return image.id

    @classmethod
    async def get_all(cls):
        async with new_session() as session:
            query = select(ImageOrm)
            result = await session.execute(query)
            result = result.scalars().all()
            images = [SImage.parse_obj(images_model) for images_model in result]
            return images
