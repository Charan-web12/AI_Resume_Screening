from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_WEIGHTS = {
    "skill_weight": 0.60,
    "text_weight": 0.30,
    "experience_weight": 0.10
}

def calculate_text_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes cosine similarity of TF-IDF vectors between resume text and JD text.
    Uses unigrams and bigrams with English stop-words.
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
        
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        sim_score = float(sim_matrix[0][0])
        # Rescale / clip to [0.0, 1.0]
        return max(0.0, min(1.0, sim_score))
    except Exception:
        # Fallback keyword overlap if vectorizer fails on empty vocabulary
        jd_words = set(jd_text.lower().split())
        res_words = set(resume_text.lower().split())
        if not jd_words:
            return 0.0
        overlap = len(jd_words.intersection(res_words)) / len(jd_words)
        return min(1.0, overlap)

def match_candidate_to_jd(
    candidate_skills: List[str],
    resume_cleaned_text: str,
    candidate_experience_years: float,
    jd_required_skills: List[str],
    jd_cleaned_text: str,
    jd_min_experience_years: float = 3.0,
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Compares candidate against Job Description:
    - Calculates Skill Match %
    - Identifies Matched, Missing, and Additional skills
    - Calculates TF-IDF Text Cosine Similarity
    - Evaluates Experience Qualification
    - Computes Final Weighted Match Percentage
    - Generates Explainability Metadata
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
        
    skill_w = weights.get("skill_weight", 0.60)
    text_w = weights.get("text_weight", 0.30)
    exp_w = weights.get("experience_weight", 0.10)
    
    # Normalize weights so they sum to 1.0
    total_w = skill_w + text_w + exp_w
    if total_w > 0:
        skill_w /= total_w
        text_w /= total_w
        exp_w /= total_w
    else:
        skill_w, text_w, exp_w = 0.60, 0.30, 0.10

    # 1. Skill Overlap
    cand_skill_set = set(candidate_skills)
    req_skill_set = set(jd_required_skills)
    
    matched_skills = sorted(list(cand_skill_set.intersection(req_skill_set)))
    missing_skills = sorted(list(req_skill_set.difference(cand_skill_set)))
    additional_skills = sorted(list(cand_skill_set.difference(req_skill_set)))
    
    if len(req_skill_set) > 0:
        skill_score = len(matched_skills) / len(req_skill_set)
    else:
        skill_score = 1.0 if len(matched_skills) > 0 else 0.5
        
    # 2. Text Cosine Similarity
    text_sim_score = calculate_text_similarity(resume_cleaned_text, jd_cleaned_text)
    
    # 3. Experience Score
    target_exp = max(jd_min_experience_years, 1.0)
    if candidate_experience_years >= target_exp:
        exp_score = 1.0
    else:
        exp_score = max(0.2, candidate_experience_years / target_exp)
        
    # 4. Final Score (0 - 100%)
    overall_score = round(
        (skill_w * skill_score + text_w * text_sim_score + exp_w * exp_score) * 100, 
        1
    )
    # Ensure bounds
    overall_score = max(0.0, min(100.0, overall_score))
    
    # 5. Explainability Breakdown
    skill_points = round(skill_w * skill_score * 100, 1)
    text_points = round(text_w * text_sim_score * 100, 1)
    exp_points = round(exp_w * exp_score * 100, 1)
    
    # Generate human-readable narrative verdict
    if overall_score >= 80:
        tier = "High Match"
        summary_verdict = f"Strong candidate with {len(matched_skills)} of {len(req_skill_set)} required skills and solid domain overlap."
    elif overall_score >= 60:
        tier = "Moderate Match"
        summary_verdict = f"Good foundational profile meeting {len(matched_skills)}/{len(req_skill_set)} requirements. Upskilling needed for {', '.join(missing_skills[:3])}."
    else:
        tier = "Low Match"
        summary_verdict = f"Significant gaps in required stack (missing {len(missing_skills)} key skills including {', '.join(missing_skills[:3])})."

    explanation = {
        "tier": tier,
        "summary": summary_verdict,
        "weights_used": {
            "skill_weight": round(skill_w, 2),
            "text_weight": round(text_w, 2),
            "experience_weight": round(exp_w, 2)
        },
        "breakdown": {
            "skill_match": {
                "score_percent": round(skill_score * 100, 1),
                "weighted_points": skill_points,
                "matched_count": len(matched_skills),
                "total_required": len(req_skill_set)
            },
            "text_similarity": {
                "score_percent": round(text_sim_score * 100, 1),
                "weighted_points": text_points,
                "cosine_similarity": round(text_sim_score, 4)
            },
            "experience": {
                "score_percent": round(exp_score * 100, 1),
                "weighted_points": exp_points,
                "candidate_years": candidate_experience_years,
                "target_years": target_exp
            }
        },
        "formula": f"Final Score ({overall_score}%) = ({skill_w:.2f} × {skill_score*100:.1f}%) + ({text_w:.2f} × {text_sim_score*100:.1f}%) + ({exp_w:.2f} × {exp_score*100:.1f}%)"
    }
    
    return {
        "overall_score": overall_score,
        "skill_score": round(skill_score * 100, 1),
        "text_similarity_score": round(text_sim_score * 100, 1),
        "experience_score": round(exp_score * 100, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "explanation": explanation
    }
