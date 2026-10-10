import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)    
UPLOAD_FOLDER = os.path.join(
BASE_DIR,
"static",
"uploads",
"profiles"
)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "lifeos_secret_key_2026"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "instance",
            "lifeos.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )