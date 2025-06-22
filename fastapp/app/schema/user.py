from datetime import date, datetime

from pydantic import BaseModel, EmailStr
from typing import Union

class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str
    role: str
    passport: Union[str, None] = None
    date_of_birth: Union[date, None] = None
    gender: Union[str, None] = None
    is_active: bool = True


class UserOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: str
    passport: Union[str, None] = None
    date_of_birth: Union[date, None] = None
    gender: Union[str, None] = None
    is_active: bool
    created_at: datetime






class UserInUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone_number: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    role: Union[str, None] = None
    passport: Union[str, None] = None
    date_of_birth: Union[date, None] = None
    gender: Union[str, None] = None
    is_active: Union[bool, None] = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str

