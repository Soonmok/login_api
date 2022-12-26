import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class SMS(Base):
    __tablename__ = "sms"

    sms_id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = relationship("phone", backref="users")
    auth_code = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
