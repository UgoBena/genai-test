from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from invoice_extractor.extractor import InvoiceExtractor

app = FastAPI()

# Serve HTML from "static" directory
app.mount("/static", StaticFiles(directory="invoice_extractor/static"), name="static")


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_content = await file.read()
    result = InvoiceExtractor().process(file_content)
    return JSONResponse(content=result)


@app.get("/")
async def main():
    return FileResponse("static/index.html")
