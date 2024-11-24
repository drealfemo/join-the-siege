import magic
from pathlib import Path


ALLOWED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "application/pdf",
    "application/zip",
    "application/json",
    "application/text",
}


def allowed_file(file_data: bytes) -> bool:
    mime_detector = magic.Magic(mime=True)
    mime_type = mime_detector.from_buffer(file_data)
    return mime_type in ALLOWED_MIME_TYPES


def load_file(filename: Path) -> bytes:
    with open(filename, "rb") as f:
        return f.read()
