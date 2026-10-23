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
from fastapi import Response
from app.utils.cache import cache_get, cache_set, cache_delete

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=ProfileOut)
def get_profile(user_id: uuid.UUID, db: Session = Depends(get_db)):
    key = f"profile:{user_id}"
    cached = cache_get(key)
    if cached is not None:
        return Response(content=cached, media_type="application/json",
                        headers={"X-Cache": "HIT"})

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    follow_repo = FollowRepository(db)
    profile = ProfileOut.model_validate({
        "user": user,
        "posts": PostRepository(db).get_by_owner(user_id),
        "follower_count": follow_repo.follower_count(user_id),
        "following_count": follow_repo.following_count(user_id),
    }, from_attributes=True)

    payload = profile.model_dump_json()
    cache_set(key, payload, ttl=30)
    return Response(content=payload, media_type="application/json",
                    headers={"X-Cache": "MISS"})


@router.post("/me/avatar", response_model=UserOut)
def upload_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    image_bytes = file.file.read()
    avatar_url = upload_image(image_bytes, file.filename, file.content_type)
    user = UserRepository(db).update_avatar(current_user.id, avatar_url)
    cache_delete(f"profile:{current_user.id}")
    return user

