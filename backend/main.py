from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo
import io
import os

app = FastAPI(title="MarkItDown Web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8000",
        "https://markitdown-ui.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))
md = MarkItDown()

@app.get("/")
def health():
    return {"status": "ok", "message": "MarkItDown Web API"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "No file provided")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File too large. Max size is {MAX_FILE_SIZE // (1024*1024)}MB")

    try:
        result = md.convert(io.BytesIO(content), stream_info=StreamInfo(filename=file.filename))
    except Exception as e:
        raise HTTPException(400, f"Conversion failed: {str(e)}")

    name = file.filename.rsplit(".", 1)[0] + ".md"
    return StreamingResponse(
        io.BytesIO(result.text_content.encode("utf-8")),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
