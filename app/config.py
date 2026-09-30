import os


class Config:
    APP_NAME = "AniVora Cloud Phone"
    VERSION = "0.1.0"

    HOST = os.getenv(
        "ANIVORA_CLOUD_PHONE_HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "ANIVORA_CLOUD_PHONE_PORT",
            "8000"
        )
    )

    DATA_DIR = os.getenv(
        "ANIVORA_CLOUD_PHONE_DATA",
        "data"
    )
