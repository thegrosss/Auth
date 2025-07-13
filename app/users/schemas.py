from pydantic import BaseModel, Field, EmailStr
import re

class UserModelAdd(BaseModel):
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(min_length=5, max_length=20, description="Пароль, от 3 до 50 символов")
    phone_number: str = Field(description="Номер телефона, начиная с '+'")

class UserSchema(BaseModel):
    id: int
    first_name: str = Field(min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    is_user: bool = True
    is_student: bool = False
    is_teacher: bool = False

class UserAuth(BaseModel):
    email: EmailStr = Field(description="Электронная почта")
    password: str = Field(description="Пароль")

class UserID(BaseModel):
    message : str = "Вы успешно зарегистрировались"
    id: int

def validate_phone_number(phone_number: str) -> str:
    if re.match(r'^\+\d{5,15}$', phone_number):
        return phone_number
    else:
        raise ValueError("Номер телефона должен начинаться с '+' и иметь от 5 до 15 цифр")