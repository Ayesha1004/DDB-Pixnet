"""
Temporary stand-in for minio_client.py while MinIO's image can't be pulled.

Same function name and signature as minio_client.upload_image, so swapping
back later is a one-line import change in routers/posts.py.
Files are saved under server/uploads/ and served by FastAPI at /uploads/...
"""

import os
import uuid

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_image(file_bytes: bytes, original_filename: str, content_type: str) -> str:
    extension = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "jpg"
    filename = f"{uuid.uuid4()}.{extension}"

    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(file_bytes)

    return f"{PUBLIC_BASE_URL}/uploads/{filename}"
