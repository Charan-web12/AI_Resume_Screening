import io
from pathlib import Path
from typing import Union
from pypdf import PdfReader
from .cleaner import clean_text

def extract_text_from_pdf(source: Union[str, Path, bytes, io.BytesIO]) -> str:
    """
    Extracts text from a PDF file path or byte stream using pypdf.
    Returns cleaned text.
    """
    try:
        if isinstance(source, (str, Path)):
            reader = PdfReader(str(source))
        elif isinstance(source, bytes):
            reader = PdfReader(io.BytesIO(source))
        else:
            reader = PdfReader(source)
            
        extracted_pages = []
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_pages.append(page_text)
                
        raw_text = "\n\n".join(extracted_pages)
        return clean_text(raw_text)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF document: {str(e)}")
