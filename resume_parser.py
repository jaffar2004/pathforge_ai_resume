"""Extract text from PDF, DOCX or TXT resumes."""
from pathlib import Path

def extract_resume_text(uploaded_file) -> str:
    name = (uploaded_file.name or "").lower()
    raw = uploaded_file.getvalue()
    if name.endswith(".pdf"):
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if name.endswith(".docx"):
        from docx import Document
        import io
        doc = Document(io.BytesIO(raw))
        return "\n".join(p.text for p in doc.paragraphs)
    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="replace")
    raise ValueError("Please upload a PDF, DOCX or TXT file.")
