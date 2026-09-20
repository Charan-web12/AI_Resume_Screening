import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_load_samples_and_rankings():
    # 1. Load sample dataset
    load_res = client.post("/api/load-samples")
    assert load_res.status_code == 200
    data = load_res.json()
    assert data["candidate_count"] == 5
    assert len(data["rankings"]) == 5
    
    # 2. Check that rankings are strictly ordered by overall_score descending
    rankings = data["rankings"]
    scores = [r["overall_score"] for r in rankings]
    assert scores == sorted(scores, reverse=True)
    
    # Candidate #1 should be Rahul Sharma (strong ML engineer)
    assert rankings[0]["candidate_name"] == "Rahul Sharma"
    assert rankings[0]["overall_score"] >= 70
    
    # Check that explanation is present
    assert "explanation" in rankings[0]
    assert "matched_skills" in rankings[0]
    assert "missing_skills" in rankings[0]

def test_custom_jd_and_analyze():
    # Submit custom JD
    jd_payload = {
        "title": "Frontend React Specialist",
        "description": "Looking for a React developer with TypeScript, HTML5, CSS3, Vite, and Tailwind CSS. 1+ years experience.",
        "min_experience_years": 1.0
    }
    jd_res = client.post("/api/job-description", json=jd_payload)
    assert jd_res.status_code == 200
    jd_id = jd_res.json()["job_description"]["id"]
    
    # Analyze existing candidates against new JD
    analyze_res = client.post("/api/analyze", json={"jd_id": jd_id})
    assert analyze_res.status_code == 200
    rankings = analyze_res.json()["rankings"]
    
    # For Frontend React JD, Sneha Rao or Priya Patel should rank at the top
    top_candidate = rankings[0]["candidate_name"]
    assert top_candidate in ["Sneha Rao", "Priya Patel"]
