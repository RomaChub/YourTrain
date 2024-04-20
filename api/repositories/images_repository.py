from api.chemas.SImages import SImageAdd
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
