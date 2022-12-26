from datetime import datetime

from pydantic import BaseModel


class SmsIn(BaseModel):
    phone: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


class SmsCreate(SmsIn):
    auth_code: str

    class Config:
        orm_mode = True
