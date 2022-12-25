from typing import Any

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..db.models.user import User
from ..db.schemas.user import UserCreate
from .base import BaseService


class UsersService(BaseService[User, UserCreate, Any]):
    def __init__(self, db_session: Session):
        super(UsersService, self).__init__(User, db_session)

    def create(self, obj: UserCreate) -> User:
        user = self.db_session.query(User).get(obj.user_id)
        if user is None:
            raise HTTPException(
                status_code=400,
                detail=f"Store with userId = {obj.user_id} not found.",
            )
        return super(UsersService, self).create(obj)

    def get_user_by_id(self, user_id):
        return self.db_session.query(User).filter(User.id == user_id).one_or_none()

    def check_if_user_exists(self, email, phone):
        return self.db_session.query(User).filter(
            or_(User.email == email, User.phone == phone)).one_or_none()

