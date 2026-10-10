import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.schema import UserOut, FollowOut
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.models import User
from app.services import follow_service

router = APIRouter(prefix="/follows", tags=["follows"])


@router.post("/{user_id}", response_model=FollowOut, status_code=status.HTTP_201_CREATED)
def follow(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_service.follow_user(db, current_user.id, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow_service.unfollow_user(db, current_user.id, user_id)


@router.get("/{user_id}/followers", response_model=list[UserOut])
def followers(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return follow_service.list_followers(db, user_id)


@router.get("/{user_id}/following", response_model=list[UserOut])
def following(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return follow_service.list_following(db, user_id)