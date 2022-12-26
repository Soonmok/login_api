from datetime import datetime, timedelta
from random import randint

from sqlalchemy.orm import Session

from app.db.models.sms import SMS
from app.db.schemas.sms import SmsCreate


def generate_auth_code() -> str:
    return str(randint(100000, 999999))


class SmsService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, sms_create: SmsCreate) -> SMS:
        sms = SMS(**sms_create.dict())
        self.db_session.add(sms)
        self.db_session.commit()
        return sms

    def validate_sms_code(self, phone, auth_code) -> bool:
        try:
            expire = datetime.utcnow() - timedelta(minutes=5)
            sms_record = self.db_session.query(SMS) \
                .filter(SMS.phone == phone, SMS.created_at > expire) \
                .order_by(SMS.created_at.desc()).first()
            return True if sms_record.auth_code == auth_code else False
        except Exception as e:
            print(e)
            return False
