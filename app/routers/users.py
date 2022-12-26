from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.models.user import User, Token
from app.db.schemas.user import UserOut, UserCreate, UserIn, UserPasswordUpdateIn
from app.db.session import get_session
from app.dependencies import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user
from app.services import get_users_service, get_sms_service

router = APIRouter()


@router.post('/users/signup', tags=["users"], summary="회원 가입", response_model=UserOut)
async def create_user(user_in: UserIn,
                      users_service=Depends(get_users_service),
                      sms_service=Depends(get_sms_service)):
    # 이미 유저가 존재하는지 파악
    if users_service.check_if_user_already_exists(user_in.email, user_in.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist",
        )

    # sms_code가 유효한지 파악
    if not sms_service.validate_sms_code(user_in.phone, user_in.sms_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SMS code is not valid",
        )
    # DB에 유저 생성
    user_create = UserCreate(**user_in.dict())
    user = users_service.create(user_create)
    return user


@router.get("/users/me", tags=["users"], summary="내 정보 조회", response_model=UserOut)
async def read_user_me(user: User = Depends(get_current_user)):
    return user


@router.patch("/users/edit_password", tags=["users"], summary="비밀번호 수정 및 토큰 발급", response_model=Token)
async def update_password(user_password_update_in: UserPasswordUpdateIn,
                          users_service=Depends(get_users_service),
                          sms_service=Depends(get_sms_service)):
    # 이미 유저가 존재하는지 파악
    if not users_service.check_if_user_already_exists(user_password_update_in.email, user_password_update_in.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist",
        )

    # sms_code가 유효한지 파악
    if not sms_service.validate_sms_code(user_password_update_in.phone, user_password_update_in.sms_code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SMS code is not valid",
        )

    # DB에 유저 정보 업데이트
    user = users_service.update_password(user_password_update_in.email, user_password_update_in.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", tags=["auth"], summary="엑세스 토큰 생성 (login)", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db_session: Session = Depends(get_session)):
    # form_data의 username은 유저별 구분자이며, 여기서는 email로 구분하도록 한다.
    user = authenticate_user(db_session=db_session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
