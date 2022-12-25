from typing import Any

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..db.models.user import User
from ..db.schemas.user import UserCreate


class UsersService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user_create: UserCreate) -> User:
        user = User(**user_create.dict())
        self.db_session.add(user)
        self.db_session.commit()
        return user

    def get_user_by_id(self, user_id):
        return self.db_session.query(User).filter(User.id == user_id).one_or_none()

    def check_if_user_already_exists(self, email, phone):
        return self.db_session.query(User).filter(
            or_(User.email == email, User.phone == phone)).one_or_none()
