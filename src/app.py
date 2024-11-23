from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.classifier import classify_file
from src.utils import allowed_file

app = FastAPI()


# Endpoint to classify files based on their content
@app.post("/classify_file")
async def classify_file_route(file: UploadFile = File(None)) -> JSONResponse:
    if file is None:
        raise HTTPException(
            status_code=400,
            detail="No file was provided in the request. Please upload a file.",
        )

    try:
        file_content = await file.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to read file")

    if not allowed_file(file_content):
        raise HTTPException(status_code=400, detail="Filetype not allowed")

    try:
        file_class = classify_file(file)
        return JSONResponse(content={"file_class": file_class})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@app.get("/")
async def root() -> JSONResponse:
    """service is alive endpoint"""
    return JSONResponse(
        content={
            "message": "File Classifier API is running. Use /classify_file endpoint to classify files."
        }
    )
