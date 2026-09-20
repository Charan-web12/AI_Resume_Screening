import pytest
from backend.nlp import (
    extract_skills,
    extract_jd_skills,
    extract_candidate_info,
    extract_name,
    extract_email,
    extract_phone,
    extract_experience_years
)

def test_extract_skills_normalization():
    text = "Hands-on experience with Python 3, ReactJS, K8s, and Amazon Web Services. Also used PostgreSQL, Docker, and Scikit-Learn."
    result = extract_skills(text)
    skills = result["all_skills"]
    
    assert "Python" in skills
    assert "React" in skills
    assert "Kubernetes" in skills
    assert "AWS" in skills
    assert "PostgreSQL" in skills
    assert "Docker" in skills
    assert "Scikit-Learn" in skills

def test_extract_candidate_info():
    sample_text = """
    Rahul Sharma
    Senior AI & Machine Learning Engineer | rahul.sharma@example.com | +1 (555) 234-5678
    
    Professional Summary
    6+ years of experience developing machine learning models and NLP applications.
    
    Education
    M.S. in Computer Science, Stanford University
    B.Tech in Computer Engineering, IIT Delhi
    """
    info = extract_candidate_info(sample_text)
    assert info["name"] == "Rahul Sharma"
    assert info["email"] == "rahul.sharma@example.com"
    assert info["phone"] == "+1 (555) 234-5678"
    assert info["experience_years"] >= 6.0
    assert any("Computer Science" in ed for ed in info["education"])

def test_extract_jd_skills():
    jd = """
    Required:
    Proficiency in Python, SQL, Machine Learning, and AWS.
    
    Nice to have:
    Kubernetes and Docker.
    """
    extracted = extract_jd_skills(jd)
    assert "Python" in extracted["all_skills"]
    assert "SQL" in extracted["all_skills"]
    assert "Machine Learning" in extracted["all_skills"]
    assert "AWS" in extracted["all_skills"]
    assert len(extracted["required_skills"]) > 0
