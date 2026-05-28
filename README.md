# MarkItDown Web

A full-stack web app that converts uploaded files to Markdown using [Microsoft MarkItDown](https://github.com/microsoft/markitdown).

**Frontend:** Vanilla JS (Vercel)  
**Backend:** FastAPI (Render)  
**Conversion:** MarkItDown Python library

## Live Demo

- Frontend: https://markitdown-ui.vercel.app
- Backend API: https://markitdown-api.onrender.com

## Supported Formats

PDF, DOCX, PPTX, XLSX, XLS, images (OCR), audio, HTML, CSV, JSON, XML, EPUB, ZIP, plain text.

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (just open in browser or serve)
cd frontend
python -m http.server 5173
```

Open http://localhost:5173 — the frontend points to `http://localhost:8000` by default.
