import os
import secrets

from PIL import Image
from flask import current_app


def save_profile_picture(uploaded_file):
    """
    Save uploaded profile image and resize it.
    Returns saved filename.
    """

    if uploaded_file is None:
        return "default.png"

    random_hex = secrets.token_hex(8)

    _, file_ext = os.path.splitext(uploaded_file.filename)

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    file_ext = file_ext.lower()

    if file_ext not in allowed_extensions:
        return "default.png"

    filename = random_hex + file_ext

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "profiles"
    )

    os.makedirs(upload_folder, exist_ok=True)

    picture_path = os.path.join(
        upload_folder,
        filename
    )

    image = Image.open(uploaded_file)

    image.thumbnail((300, 300))

    image.save(picture_path)

    return filename