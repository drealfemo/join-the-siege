import pytest
from pathlib import Path

from src.app import allowed_file
from src.utils import load_file

FIXTURES_FILES_DIR = Path(__file__).resolve().parents[0] / "fixtures" / "files"


def get_allowed_files():
    return [
        (load_file(fn), True)
        for fn in (FIXTURES_FILES_DIR / "allowed").glob("**/*")
        if fn.is_file()
    ]


@pytest.mark.parametrize("file_content, expected", get_allowed_files())
def test_allowed_file(file_content, expected):
    assert allowed_file(file_content) == expected
