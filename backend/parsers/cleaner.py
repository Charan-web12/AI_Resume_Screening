import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Normalizes extracted raw resume or JD text:
    - Normalizes unicode characters (NFKD)
    - Replaces bullet points, fancy quotes, dashes with standard ASCII
    - Collapses repeated whitespaces while preserving meaningful paragraph breaks
    """
    if not text:
        return ""
    
    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)
    
    # Replace common bullet characters with a clean hyphen or space
    bullet_chars = ["•", "·", "▪", "▫", "◆", "❖", "★", "✓", "✔", "➤", "➢", "►", "■", "–", "—", "\x7f", "\x80", "\x96", "\x97"]
    for b in bullet_chars:
        text = text.replace(b, " ")
        
    # Filter non-printable ASCII control characters except newline and tab
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', ' ', text)
        
    # Replace fancy quotes
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    
    # Replace non-breaking spaces and tabs
    text = text.replace("\xa0", " ").replace("\t", " ")
    
    # Normalize line breaks: replace multiple consecutive empty lines with double newline
    lines = [line.strip() for line in text.splitlines()]
    # Remove excessive blank lines
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if line:
            # Collapse multiple spaces inside the line
            collapsed_line = re.sub(r"[ ]{2,}", " ", line)
            cleaned_lines.append(collapsed_line)
            prev_blank = False
        elif not prev_blank:
            cleaned_lines.append("")
            prev_blank = True
            
    cleaned_text = "\n".join(cleaned_lines).strip()
    return cleaned_text

def extract_sections(text: str) -> dict:
    """
    Splits resume into rough sections based on common headings:
    Experience, Education, Skills, Projects, Certifications, Summary
    """
    section_patterns = {
        "experience": r"(?:work\s+experience|professional\s+experience|employment|experience|work\s+history)",
        "education": r"(?:education|academic\s+background|academics|qualifications)",
        "skills": r"(?:skills|technical\s+skills|core\s+competencies|technologies|tools)",
        "projects": r"(?:projects|key\s+projects|academic\s+projects)",
        "certifications": r"(?:certifications|certificates|licenses|courses)",
        "summary": r"(?:summary|professional\s+summary|objective|profile|about\s+me)"
    }
    
    sections = {k: "" for k in section_patterns.keys()}
    sections["other"] = text
    return sections
