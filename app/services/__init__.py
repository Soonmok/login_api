from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.sms import SmsService
from app.services.users import UsersService


def get_users_service(db_session: Session = Depends(get_session)) -> UsersService:
    return UsersService(db_session)


def get_sms_service(db_session: Session = Depends(get_session)) -> SmsService:
    return SmsService(db_session)


__all__ = ("get_users_service", "get_sms_service")
