from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from markitdown import MarkItDown
import tempfile
import io
import os

app = FastAPI(title="MarkItDown Web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    suffix = os.path.splitext(file.filename)[1] or ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(content)
        tmp.close()
        result = md.convert(tmp.name)
    except Exception as e:
        raise HTTPException(400, f"Conversion failed: {str(e)}")
    finally:
        os.unlink(tmp.name)

    name = file.filename.rsplit(".", 1)[0] + ".md"
    return StreamingResponse(
        io.BytesIO(result.text_content.encode("utf-8")),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
