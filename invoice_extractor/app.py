from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from invoice_extractor.extractor import InvoiceExtractor

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
# Serve HTML from "static" directory
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDFs are allowed.")

    file_content = await file.read()
    result = InvoiceExtractor().process(file_content)
    return JSONResponse(content=result)


@app.get("/")
async def main():
    return FileResponse(BASE_DIR / "static/index.html")
