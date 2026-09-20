import pytest
from backend.nlp import match_candidate_to_jd, calculate_text_similarity

def test_text_similarity():
    text1 = "Senior Python engineer building microservices with FastAPI, Docker, and PostgreSQL on AWS."
    text2 = "Looking for a Python developer experienced with Docker, FastAPI, and AWS cloud."
    unrelated = "Pastry chef with expertise in French baking, croissants, and sourdough cakes."
    
    sim_high = calculate_text_similarity(text1, text2)
    sim_low = calculate_text_similarity(text1, unrelated)
    
    assert sim_high > 0.10
    assert sim_high > sim_low

def test_matcher_scoring_and_explainability():
    candidate_skills = ["Python", "Docker", "AWS", "Git", "SQL"]
    resume_text = "Experienced software engineer with 5 years in Python, Docker, AWS, and SQL backend systems."
    cand_exp = 5.0
    
    jd_skills = ["Python", "Docker", "AWS", "Kubernetes", "PyTorch"]
    jd_text = "Seeking Senior AI / Cloud Engineer with Python, Docker, AWS, Kubernetes, PyTorch. 4+ years required."
    
    match = match_candidate_to_jd(
        candidate_skills=candidate_skills,
        resume_cleaned_text=resume_text,
        candidate_experience_years=cand_exp,
        jd_required_skills=jd_skills,
        jd_cleaned_text=jd_text,
        jd_min_experience_years=4.0
    )
    
    assert "overall_score" in match
    assert match["overall_score"] > 50
    assert "Python" in match["matched_skills"]
    assert "AWS" in match["matched_skills"]
    assert "Docker" in match["matched_skills"]
    assert "Kubernetes" in match["missing_skills"]
    assert "PyTorch" in match["missing_skills"]
    assert "Git" in match["additional_skills"]
    
    # Check explanation structure
    explanation = match["explanation"]
    assert "breakdown" in explanation
    assert "formula" in explanation
    assert explanation["breakdown"]["skill_match"]["matched_count"] == 3
    assert explanation["breakdown"]["skill_match"]["total_required"] == 5
