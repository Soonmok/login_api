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


class UserCreate(BaseModel):
    nickname: str
    password: str
    name: str
    phone: str
    email: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class UserPasswordUpdateIn(BaseModel):
    email: str
    phone: str
    sms_code: str
    password: str


class UserOut(BaseModel):
    user_id: UUID4
    nickname: str
    name: str
    phone: str
    email: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
