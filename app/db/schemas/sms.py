from datetime import datetime

from pydantic import BaseModel


class SmsIn(BaseModel):
    phone: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "phone": "01012345678"
            }
        }


class SmsCreate(SmsIn):
    auth_code: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "phone": "01012345678",
                "auth_code": "123456"
            }
        }
