from app.core.database import SessionLocal
from sqlalchemy import select

from app.users.models import User
from app.users.schemas import UserModelAdd, UserSchema
from app.core.security import get_password_hash

class UserDAO:
    @classmethod
    async def get_all_users(cls) -> list[UserSchema]:
        async with SessionLocal() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filters) -> User:
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

    @classmethod
    async def change_role(cls, id: int,
                          role: str,
                          value: bool):
        async with SessionLocal() as session:
            result = await session.execute(select(User).filter_by(id=id))
            user = result.scalar_one_or_none()
            setattr(user, role, value)
            print("Изменено")
            await session.commit()