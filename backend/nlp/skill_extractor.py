import re
from typing import List, Dict, Set, Tuple
from .taxonomy import SKILL_CATEGORIES, SKILL_ALIASES, SKILL_TO_CATEGORY

# Sort aliases by length descending so longer multi-word phrases match first
SORTED_ALIASES = sorted(SKILL_ALIASES.keys(), key=lambda x: len(x), reverse=True)

def extract_skills(text: str) -> Dict[str, any]:
    """
    Extracts skills from text, normalizes to canonical names, and groups by category.
    Returns:
    {
        "all_skills": List[str],
        "skills_by_category": Dict[str, List[str]]
    }
    """
    if not text:
        return {"all_skills": [], "skills_by_category": {}}
        
    found_canonical_skills: Set[str] = set()
    text_lower = " " + text.lower() + " "
    
    # Pre-clean punctuation that could stick to words, but preserve +, #, ., /
    cleaned_text_lower = re.sub(r"[,;:\(\)\[\]\{\}\<\>\"\*\|\n]", " ", text_lower)
    
    for alias in SORTED_ALIASES:
        canonical = SKILL_ALIASES[alias]
        
        # Build boundary-safe regex
        # Special characters like +, #, ., / need escaping
        escaped_alias = re.escape(alias)
        
        # Word boundary: \b works for words, but for C++, C#, CI/CD, .NET we need custom lookaround
        pattern = rf"(?<![a-zA-Z0-9_]){escaped_alias}(?![a-zA-Z0-9_])"
        
        if re.search(pattern, cleaned_text_lower):
            found_canonical_skills.add(canonical)
            
    # Also check canonical skill names directly
    for category, skill_list in SKILL_CATEGORIES.items():
        for skill in skill_list:
            escaped_skill = re.escape(skill.lower())
            pattern = rf"(?<![a-zA-Z0-9_]){escaped_skill}(?![a-zA-Z0-9_])"
            if re.search(pattern, cleaned_text_lower):
                found_canonical_skills.add(skill)

    sorted_skills = sorted(list(found_canonical_skills))
    
    # Categorize
    by_category: Dict[str, List[str]] = {}
    for skill in sorted_skills:
        cat = SKILL_TO_CATEGORY.get(skill.lower(), "Other Technical Skills")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(skill)
        
    return {
        "all_skills": sorted_skills,
        "skills_by_category": by_category
    }

def extract_jd_skills(jd_text: str) -> Dict[str, any]:
    """
    Analyzes Job Description text:
    - Extracts all skills
    - Separates required vs optional/preferred skills based on context headings
    - Extracts key technology keywords
    """
    cleaned_jd = text = jd_text
    
    # Look for "preferred", "nice to have", "bonus", "optional" sections
    optional_patterns = [
        r"(?:nice\s+to\s+have|preferred\s+qualifications|bonus|plus|optional|good\s+to\s+have)[\s\S]*?(?:requirements|responsibilities|$)",
    ]
    
    optional_text = ""
    for pat in optional_patterns:
        match = re.search(pat, jd_text, re.IGNORECASE)
        if match:
            optional_text += " " + match.group(0)
            
    extracted_all = extract_skills(jd_text)
    all_skills = extracted_all["all_skills"]
    
    optional_skills = []
    if optional_text:
        extracted_opt = extract_skills(optional_text)
        optional_skills = extracted_opt["all_skills"]
        
    required_skills = [s for s in all_skills if s not in optional_skills]
    
    # If all ended up optional (edge case), make all required
    if not required_skills and all_skills:
        required_skills = all_skills
        optional_skills = []
        
    return {
        "all_skills": all_skills,
        "required_skills": required_skills,
        "optional_skills": optional_skills,
        "skills_by_category": extracted_all["skills_by_category"],
        "total_required": len(required_skills)
    }
