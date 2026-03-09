"""Extract text from lab result PDFs using pdfplumber."""
from pathlib import Path
import pdfplumber


def extract_text(file_path: str | Path) -> str:
    """Extract all text from a PDF file."""
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n\n".join(text_parts)
