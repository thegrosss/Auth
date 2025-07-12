from app.database import Model
from sqlalchemy.orm import Mapped, mapped_column

class User(Model):
    __tablename__: str = "Users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True)
    is_student: Mapped[bool] = mapped_column(default=False)
    is_teacher: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)