from datetime import datetime
from pydantic import BaseModel
from pydantic.types import UUID4


class UserIn(BaseModel):
    nickname: str
    password: str
    name: str
    phone: str
    email: str
    sms_code: str
    created_at: datetime = datetime.utcnow()

    class Config:
        schema_extra = {
            "example": {
                "nickname": "johndoe",
                "password": "password1",
                "name": "john doe",
                "phone": "01012345678",
                "email": "john@gmail.com",
                "sms_code": "123456"
            }
        }


class UserCreate(BaseModel):
    nickname: str
    password: str
    name: str
    phone: str
    email: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "nickname": "johndoe",
                "password": "password1",
                "name": "john doe",
                "phone": "01012345678",
                "email": "john@gmail.com"
            }
        }


class UserPasswordUpdateIn(BaseModel):
    email: str
    phone: str
    sms_code: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "password": "password1",
                "phone": "01012345678",
                "email": "john@gmail.com",
                "sms_code": "123456"
            }
        }


class UserOut(BaseModel):
    user_id: UUID4
    nickname: str
    name: str
    phone: str
    email: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": "a0eebc99",
                "nickname": "johndoe",
                "name": "john doe",
                "phone": "01012345678",
                "email": "john@gmail.com",
                "created_at": "2021-01-01 00:00:00"
            }
        }


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
