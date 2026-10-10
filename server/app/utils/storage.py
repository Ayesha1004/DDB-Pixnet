import os

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")  # "local" or "s3"

if STORAGE_BACKEND == "s3":
    from .s3_storage import upload_image
else:
    from .local_storage import upload_image

__all__ = ["upload_image"]