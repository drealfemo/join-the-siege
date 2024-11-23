from fastapi import UploadFile

FILECLASSES = ["drivers_license", "bank_statement", "invoice"]


def classify_file(file: UploadFile) -> str:
    # this is to satisfy mypy, fast api does not allow a nameless file to be uploaded
    if not (filename := file.filename):
        return "unknown"

    for f_class in FILECLASSES:
        if f_class in filename.lower():
            return f_class
    else:
        return "unknown"
