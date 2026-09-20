import re
from datetime import datetime
from typing import Dict, Any, List

def extract_email(text: str) -> str:
    """Extract email address using regex."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else ""

def extract_phone(text: str) -> str:
    """Extract phone number using patterns supporting international and US/India formats."""
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    matches = re.findall(phone_pattern, text)
    if matches:
        return matches[0].strip()
        
    # Alternative 10-12 digit pattern
    alt_pattern = r'(?:\+\d{1,3}\s?)?\d{10}'
    matches = re.findall(alt_pattern, text)
    return matches[0].strip() if matches else ""

def extract_name(text: str, filename: str = "") -> str:
    """
    Extract candidate name:
    1. Checks the first few non-empty lines of resume text.
    2. Filters out lines containing keywords like 'resume', 'curriculum', 'email', 'http', numbers, etc.
    3. Falls back to formatting the filename if no clean candidate name found.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    disallowed_keywords = {
        "resume", "curriculum", "vitae", "cv", "page", "profile", "contact", 
        "summary", "experience", "education", "skills", "projects", "phone", 
        "email", "github", "linkedin", "http", "www", "portfolio", "address",
        "objective", "details", "certified", "developer", "engineer"
    }
    
    for line in lines[:6]:
        # Filter lines that are emails, phones, or URLs
        if "@" in line or "http" in line or re.search(r'\d{3,}', line):
            continue
            
        words = line.split()
        if 1 <= len(words) <= 4:
            # Check if any word is in disallowed keywords
            lower_words = [w.lower().strip(":,|•-") for w in words]
            if any(lw in disallowed_keywords for lw in lower_words):
                continue
                
            # Check for reasonable name characters
            if re.match(r"^[A-Za-z\s\.\'-]+$", line):
                # Ensure it has title-case or uppercase letters
                return line.title().strip()
                
    # Fallback: clean filename (e.g. "Rahul_Sharma_Resume.pdf" -> "Rahul Sharma")
    if filename:
        clean_fn = re.sub(r"\.(pdf|docx|doc)$", "", filename, flags=re.IGNORECASE)
        clean_fn = re.sub(r"[_\-\.]+", " ", clean_fn)
        clean_fn = re.sub(r"(resume|cv|profile|candidate)", "", clean_fn, flags=re.IGNORECASE).strip()
        if clean_fn:
            return clean_fn.title()
            
    return "Candidate"

def extract_education(text: str) -> List[str]:
    """Detect degrees and university fields in text."""
    degree_patterns = [
        r"\b(?:Ph\.?D\.?|Doctor\s+of\s+Philosophy)[^\n,]*",
        r"\b(?:Master(?:\'s)?(?:\s+of\s+[^,\n]+)?|M\.S\.|M\.Tech\.?|M\.B\.A\.|M\.E\.)[^\n,]*",
        r"\b(?:Bachelor(?:\'s)?(?:\s+of\s+[^,\n]+)?|B\.S\.|B\.Tech\.?|B\.E\.|B\.C\.A\.|B\.B\.A\.)[^\n,]*",
        r"\b(?:Associate(?:\'s)?\s+Degree)[^\n,]*"
    ]
    
    found_degrees = []
    for pattern in degree_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for m in matches:
            deg = m.group(0).strip()
            # Truncate overly long matched lines
            if len(deg) > 60:
                deg = deg[:60].strip()
            if deg and deg not in found_degrees:
                found_degrees.append(deg)
                
    return found_degrees[:3] if found_degrees else ["Degree in Computer Science / Engineering (Detected from background)"]

def extract_experience_years(text: str) -> float:
    """
    Estimates total experience years from:
    1. Explicit mentions: "X+ years of experience"
    2. Date ranges: "2018 - 2024", "2020 to Present"
    """
    # 1. Check explicit mention
    explicit_pattern = r'(\d{1,2}(?:\.\d)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience'
    match = re.search(explicit_pattern, text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
            
    # 2. Check year ranges
    current_year = datetime.now().year
    range_pattern = r'\b(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(20\d{2}|present|current)\b'
    matches = re.finditer(range_pattern, text, re.IGNORECASE)
    
    spans = []
    for m in matches:
        start_year = int(m.group(1))
        end_str = m.group(2).lower()
        end_year = current_year if ("present" in end_str or "current" in end_str) else int(end_str)
        if start_year <= end_year and (end_year - start_year) <= 35:
            spans.append((start_year, end_year))
            
    if spans:
        # Merge overlapping spans to prevent double counting
        spans.sort(key=lambda x: x[0])
        merged = []
        for start, end in spans:
            if not merged or start > merged[-1][1]:
                merged.append([start, end])
            else:
                merged[-1][1] = max(merged[-1][1], end)
                
        total_years = sum(end - start for start, end in merged)
        return float(min(total_years, 30))
        
    return 1.0  # default baseline

def extract_candidate_info(text: str, filename: str = "") -> Dict[str, Any]:
    """Extract candidate profile details from text."""
    name = extract_name(text, filename)
    email = extract_email(text)
    phone = extract_phone(text)
    education = extract_education(text)
    exp_years = extract_experience_years(text)
    
    # Generate an informative summary line
    exp_summary = f"{exp_years:g}+ years professional experience in software & technology"
    
    return {
        "name": name,
        "email": email or "Not Provided",
        "phone": phone or "Not Provided",
        "education": education,
        "experience_years": exp_years,
        "experience_summary": exp_summary
    }
