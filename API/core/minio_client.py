from minio import Minio
from minio.error import S3Error
from .config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False 
)

def get_minio_client():
    try:
        found = minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)
        yield minio_client
    except S3Error as exc:
        raise ConnectionError(f"Could not connect to MinIO: {exc}")