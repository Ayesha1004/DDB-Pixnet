import os
import uuid

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:8333")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "anything")   # SeaweedFS ignores these unless you configure auth
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "anything")
S3_BUCKET = os.getenv("S3_BUCKET", "pixnet-images")

_s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)


def ensure_bucket_exists() -> None:
    try:
        _s3_client.head_bucket(Bucket=S3_BUCKET)
    except ClientError:
        _s3_client.create_bucket(Bucket=S3_BUCKET)


def upload_image(file_bytes: bytes, original_filename: str, content_type: str) -> str:
    extension = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "jpg"
    object_key = f"posts/{uuid.uuid4()}.{extension}"
    _s3_client.put_object(Bucket=S3_BUCKET, Key=object_key, Body=file_bytes, ContentType=content_type)
    return f"{S3_ENDPOINT}/{S3_BUCKET}/{object_key}"


