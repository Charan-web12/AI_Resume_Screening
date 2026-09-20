import pytest
from pathlib import Path
from backend.parsers import clean_text, extract_text_from_pdf, extract_text_from_docx

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"

def test_clean_text():
    raw = "Rahul  Sharma\n\n\n• Python &bull; Machine Learning\n\t\t\xa0AWS   Cloud"
    cleaned = clean_text(raw)
    assert "Rahul Sharma" in cleaned
    assert "Python" in cleaned
    assert "AWS Cloud" in cleaned

def test_pdf_parser():
    pdf_path = SAMPLE_DIR / "Rahul_Sharma_Senior_ML_Engineer.pdf"
    assert pdf_path.exists(), "Sample PDF must exist"
    text = extract_text_from_pdf(pdf_path)
    assert len(text) > 500
    assert "Rahul Sharma" in text
    assert "Python" in text
    assert "PyTorch" in text

def test_docx_parser():
    docx_path = SAMPLE_DIR / "Priya_Patel_FullStack_Engineer.docx"
    assert docx_path.exists(), "Sample DOCX must exist"
    text = extract_text_from_docx(docx_path)
    assert len(text) > 500
    assert "Priya Patel" in text
    assert "React" in text
    assert "PostgreSQL" in text
