from datetime import datetime, timezone

from app.core.database import Model
from sqlalchemy.orm import Mapped, mapped_column

class User(Model):
    __tablename__: str = "Users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    token_created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    token_updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc),
                                                       onupdate=datetime.now(timezone.utc))

    is_user: Mapped[bool] = mapped_column(default=True)
    is_student: Mapped[bool] = mapped_column(default=False)
    is_teacher: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)