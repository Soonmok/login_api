import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from typing import Any
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = sa.Column(sa.Text, nullable=False)
    password = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    phone = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
