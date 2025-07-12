from app.database import SessionLocal
from sqlalchemy import select

from app.users.models import User
from app.users.schemas import UserModelAdd
from app.users.auth import get_password_hash

class BaseDAO:
    @classmethod
    async def get_all_users(cls):
        async with SessionLocal() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with SessionLocal() as session:
            query = select(User).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, data: UserModelAdd) -> int:
        async with SessionLocal() as session:
            user_dict = data.model_dump()

            user = User(**user_dict)
            user_dict['password'] = get_password_hash(data.password)
            session.add(user)

            await session.flush()
            await session.commit()

            return user.id
