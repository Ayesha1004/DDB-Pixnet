import os
import uuid

import requests

from app.core.database import SessionLocal
from app.repository.post_repo import PostRepository

EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:8001")


def send_to_embedding_service(post_id: str, owner_id: str, image_url: str, image_bytes: bytes, filename: str, content_type: str) -> None:
    try:
        resp = requests.post(
            f"{EMBEDDING_SERVICE_URL}/embed",
            data={"post_id": post_id, "owner_id": owner_id, "image_url": image_url},
            files={"file": (filename, image_bytes, content_type)},
            timeout=30,
        )
        resp.raise_for_status()   # <-- new: raises if the embedding service returned an error

        db = SessionLocal()
        try:
            PostRepository(db).mark_embedded(uuid.UUID(post_id))
        finally:
            db.close()
    except Exception:
        pass  # embedding failing should never break the upload itself # embedding failing should never break the upload itself