import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.schema import ProfileOut, UserOut
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.models import User
from app.repository.repos import UserRepository
from app.repository.post_repo import PostRepository
from app.repository.follow_repo import FollowRepository
from app.utils.storage import upload_image

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=ProfileOut)
def get_profile(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    follow_repo = FollowRepository(db)
    return {
        "user": user,
        "posts": PostRepository(db).get_by_owner(user_id),
        "follower_count": follow_repo.follower_count(user_id),
        "following_count": follow_repo.following_count(user_id),
    }


@router.post("/me/avatar", response_model=UserOut)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    image_bytes = file.file.read()
    avatar_url = upload_image(image_bytes, file.filename, file.content_type)
    return UserRepository(db).update_avatar(current_user.id, avatar_url)