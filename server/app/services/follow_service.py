import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.repository.follow_repo import FollowRepository
from app.repository.repos import UserRepository


def follow_user(db: Session, follower_id: uuid.UUID, target_id: uuid.UUID):
    if follower_id == target_id:
        raise HTTPException(status_code=400, detail="You can't follow yourself")

    if not UserRepository(db).get_by_id(target_id):
        raise HTTPException(status_code=404, detail="User not found")

    follow_repo = FollowRepository(db)
    if follow_repo.is_following(follower_id, target_id):
        raise HTTPException(status_code=400, detail="Already following this user")

    try:
        return follow_repo.follow(follower_id, target_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already following this user")


def unfollow_user(db: Session, follower_id: uuid.UUID, target_id: uuid.UUID):
    if not FollowRepository(db).unfollow(follower_id, target_id):
        raise HTTPException(status_code=404, detail="You are not following this user")


def list_followers(db: Session, user_id: uuid.UUID):
    return FollowRepository(db).get_followers(user_id)


def list_following(db: Session, user_id: uuid.UUID):
    return FollowRepository(db).get_following(user_id)