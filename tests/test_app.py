from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.app import allowed_file, app

FIXTURES_FILES_DIR = Path(__file__).resolve().parents[0] / "fixtures" / "files"

client = TestClient(app)


def load_file(filename: Path):
    with open(filename, "rb") as f:
        return f.read()


def get_allowed_files():
    return [
        (load_file(fn), True)
        for fn in (FIXTURES_FILES_DIR / "allowed").glob("**/*")
        if fn.is_file()
    ]


@pytest.mark.parametrize("file_content, expected", get_allowed_files())
def test_allowed_file(file_content, expected):
    assert allowed_file(file_content) == expected


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "File Classifier API is running. Use /classify_file endpoint to classify files."
    }


def test_valid_file():
    """Test the classify endpoint with a valid file."""
    pdf_data = BytesIO(load_file(FIXTURES_FILES_DIR / "allowed" / "invoice_1.pdf"))
    response = client.post("/classify_file", files={"file": ("invoice.pdf", pdf_data)})
    assert response.status_code == 200
    assert response.json() == {"file_class": "invoice"}


def test_missing_file():
    response = client.post("/classify_file")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No file was provided in the request. Please upload a file."
    }


@pytest.mark.parametrize(
    "filename, content",
    [
        (
            "invoice.pdf",
            b"Hello, this is a text file.",
        ),  # wrong_data_with_valid_extension
        ("binary.dat", b"\x00\x01\x02\x03"),  # filetype not allowed
    ],
)
def test_disallowed_file(filename, content):
    response = client.post("/classify_file", files={"file": (filename, content)})
    assert response.status_code == 400
    assert response.json() == {"detail": "Filetype not allowed"}
