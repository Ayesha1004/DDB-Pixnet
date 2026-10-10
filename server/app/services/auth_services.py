from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.schema import UserCreate, UserLogin, Token
from app.core.security import verify_password, create_access_token
from app.repository.repos import UserRepository


def signup(db: Session, payload: UserCreate):
    repo = UserRepository(db)

    if repo.user_exists_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if repo.user_exists_by_username(payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    return repo.create_user(payload)


def login(db: Session, payload: UserLogin) -> Token:
    repo = UserRepository(db)
    user = repo.get_by_email(payload.email)

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(subject=str(user.id))
    return Token(access_token=access_token)
