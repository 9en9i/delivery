from minio import Minio

from delivery.settings import settings, BASE_DIR


def main():
    minio_client = Minio(
        settings.MINIO_HOSTNAME,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,
    )
    minio_client.fput_object(
        "images",
        "empty.jpg",
        BASE_DIR.parent / "static" / "empty.jpg",
    )


if __name__ == "__main__":
    main()
