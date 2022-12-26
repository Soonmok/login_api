import uuid

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID

from typing import Any, Union
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text, nullable=False)
    phone_verified = sa.Column(sa.Boolean, nullable=False, default=False)
    email = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Union[str, None] = None
