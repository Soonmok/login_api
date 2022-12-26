import os
from datetime import timedelta, datetime
from typing import Union, Optional

from fastapi import HTTPException, Depends, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models.user import TokenData, User
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from app.db.session import get_session

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.environ['JWT_SECRET_KEY']  # 코드에서 직접적으로 보이면 안되므로 환경변수로 관리

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db_session, user_id: str = None, email: str = None) -> Optional[User]:
    if user_id:
        return db_session.query(User).filter(User.user_id == user_id).one_or_none()
    elif email:
        return db_session.query(User).filter(User.email == email).one_or_none()
    else:
        return None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db_session, email: str, password: str):
    user = get_user(db_session=db_session, email=email)
    if not user or not user.phone_verified:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user(db_session=db_session, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
