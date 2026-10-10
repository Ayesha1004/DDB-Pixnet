import uuid, requests
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.utils.storage import upload_image
from app.utils.embedding_client import send_to_embedding_service

from app.core.schema import PostCreate, PostOut
from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.core.models import User
from app.repository.post_repo import PostRepository
from app.utils.storage import upload_image
#from app.utils.minio_client import upload_image
import os

EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:8001")


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostOut, status_code=201)
def create_post(
    background_tasks: BackgroundTasks,
    caption: str = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # <-- owner comes from the JWT, never from the client
):
    image_bytes = file.file.read()
    image_url = upload_image(image_bytes, file.filename, file.content_type)

    repo = PostRepository(db)
    post = repo.create(owner_id=current_user.id, caption=caption, image_url=image_url)
    background_tasks.add_task(
        send_to_embedding_service,
        str(post.id), str(current_user.id), image_url, image_bytes, file.filename, file.content_type,
    )

    return post


@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    repo = PostRepository(db)
    return repo.get_all()


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = PostRepository(db)
    post = repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = PostRepository(db)
    deleted = repo.delete(post_id, owner_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found or not yours to delete")

@router.get("/search", response_model=list[PostOut])
def search_posts(q: str, limit: int = 10, db: Session = Depends(get_db)):
    resp = requests.post(f"{EMBEDDING_SERVICE_URL}/search", json={"text": q, "limit": limit}, timeout=10)
    resp.raise_for_status()
    results = resp.json()
    repo = PostRepository(db)
    posts = [repo.get_by_id(uuid.UUID(r["post_id"])) for r in results]
    return [p for p in posts if p]
