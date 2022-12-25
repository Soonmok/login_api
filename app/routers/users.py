from fastapi import APIRouter, Depends, HTTPException, status

from app.db.schemas.user import UserOut, UserCreate
from app.services import get_users_service

router = APIRouter()


@router.post('/users/signup', tags=["users"], summary="회원 가입", response_model=UserOut)
async def create_user(user_create: UserCreate, users_service=Depends(get_users_service)):
    # querying database to check if user already exist
    if users_service.check_if_user_exists(user_create.email, user_create.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exist",
        )

    # TODO: 전화 인증 추가 필요
    # saving user to database
    user = users_service.create(user_create)
    return user


@router.get("/users/me", tags=["users"], summary="내 정보 조회", response_model=UserOut)
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
