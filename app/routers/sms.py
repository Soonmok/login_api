from fastapi import APIRouter, Depends, HTTPException, status

from app.db.schemas.sms import SmsIn, SmsCreate
from app.services import get_sms_service
from app.services.sms import generate_auth_code
import requests

router = APIRouter()


@router.post('/sms', tags=["sms"], summary="SMS 인증 코드 발송", response_model=SmsCreate)
async def send_sms(sms_in: SmsIn, sms_service=Depends(get_sms_service)):
    sms_create = sms_in
    sms_create.auth_code = generate_auth_code()
    sms = sms_service.create(sms_create)

    # TODO: SMS 발송 로직 추가 필요
    response = requests.get("http://google.com/")
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service unavailable",
        )
    # 원래는 Client가 auth_code를 보면 안되지만, 우리는 문자 메세지를 보내지 않으므로 보여준다.
    return sms
