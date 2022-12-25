from datetime import datetime
from pydantic import BaseModel
from pydantic.types import UUID4


class UserCreate(BaseModel):
    user_id: UUID4
    nickname: str
    password: str
    name: str
    phone: str
    create_at: datetime