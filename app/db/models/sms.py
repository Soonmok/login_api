import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.base import Base


class SMS(Base):
    __tablename__ = "sms"

    sms_id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = sa.Column(sa.Text, nullable=False)
    auth_code = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
