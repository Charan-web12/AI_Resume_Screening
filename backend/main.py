import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from backend.database import (
    init_db,
    save_job_description,
    get_job_description,
    get_latest_job_description,
    save_candidate,
    get_candidate,
    get_all_candidates,
    save_match_result,
    get_rankings_for_jd,
    clear_all_data
)
from backend.parsers import extract_text_from_pdf, extract_text_from_docx, clean_text
from backend.nlp import (
    extract_skills,
    extract_jd_skills,
    extract_candidate_info,
    match_candidate_to_jd,
    DEFAULT_WEIGHTS
)
from backend.data.sample_jds import SAMPLE_JOB_DESCRIPTIONS

# Setup folders
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_RESUME_DIR = BASE_DIR / "data" / "sample_resumes"

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="AI Resume Screening & Candidate Matching System",
    description="Automated resume parser, skill extractor, TF-IDF cosine matcher, and candidate ranking platform.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class JobDescriptionRequest(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Senior AI & Machine Learning Engineer"})
    description: str = Field(..., json_schema_extra={"example": "We are hiring a Senior ML Engineer with Python, PyTorch, Docker, AWS..."})
    min_experience_years: Optional[float] = 3.0
    required_skills: Optional[List[str]] = None
    optional_skills: Optional[List[str]] = None

class ScoringWeights(BaseModel):
    skill_weight: Optional[float] = 0.60
    text_weight: Optional[float] = 0.30
    experience_weight: Optional[float] = 0.10

class AnalyzeRequest(BaseModel):
    jd_id: Optional[int] = None
    candidate_ids: Optional[List[int]] = None
    weights: Optional[ScoringWeights] = None

# --- API Endpoints ---

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Resume Screening API"}

@app.get("/api/job-description/templates")
def get_sample_job_descriptions():
    """Returns available sample JD templates for quick loading."""
    return SAMPLE_JOB_DESCRIPTIONS

@app.get("/api/job-description/latest")
def get_latest_jd():
    """Fetches currently active Job Description."""
    jd = get_latest_job_description()
    if not jd:
        return {"active": False, "job_description": None}
    return {"active": True, "job_description": jd}

@app.get("/api/job-description/{jd_id}")
def get_jd_by_id(jd_id: int):
    jd = get_job_description(jd_id)
    if not jd:
        raise HTTPException(status_code=404, detail="Job description not found")
    return jd

@app.post("/api/job-description")
def submit_job_description(payload: JobDescriptionRequest):
    """
    Submits and parses a Job Description.
    Extracts required skills, optional skills, and technology keywords.
    """
    cleaned_desc = clean_text(payload.description)
    if not cleaned_desc:
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
        
    # Auto-extract skills if not explicitly supplied
    extracted = extract_jd_skills(cleaned_desc)
    req_skills = payload.required_skills if payload.required_skills is not None else extracted["required_skills"]
    opt_skills = payload.optional_skills if payload.optional_skills is not None else extracted["optional_skills"]
    
    jd_id = save_job_description(
        title=payload.title,
        description=cleaned_desc,
        required_skills=req_skills,
        optional_skills=opt_skills,
        keywords=extracted["all_skills"],
        min_experience_years=payload.min_experience_years or 3.0
    )
    
    saved_jd = get_job_description(jd_id)
    return {
        "message": "Job description created and analyzed successfully",
        "job_description": saved_jd
    }

@app.post("/api/resumes/upload")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Uploads multiple candidate resumes in PDF or DOCX format.
    Extracts raw text, candidate contact info, education, experience, and skills.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
        
    created_candidates = []
    errors = []
    
    for file in files:
        filename = file.filename
        ext = Path(filename).suffix.lower()
        
        if ext not in [".pdf", ".docx", ".doc"]:
            errors.append({"filename": filename, "error": f"Unsupported format '{ext}'. Only PDF and DOCX are supported."})
            continue
            
        file_path = UPLOAD_DIR / filename
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
            
        # Parse text based on format
        try:
            if ext == ".pdf":
                extracted_text = extract_text_from_pdf(file_path)
            else:
                extracted_text = extract_text_from_docx(file_path)
        except Exception as e:
            errors.append({"filename": filename, "error": f"Failed to parse document: {str(e)}"})
            continue
            
        cleaned = clean_text(extracted_text)
        if not cleaned:
            errors.append({"filename": filename, "error": "Could not extract readable text from document."})
            continue
            
        # Extract Information & Skills
        info = extract_candidate_info(cleaned, filename=filename)
        skills_data = extract_skills(cleaned)
        
        cand_dict = {
            "filename": filename,
            "file_type": ext.lstrip("."),
            "file_path": str(file_path),
            "name": info["name"],
            "email": info["email"],
            "phone": info["phone"],
            "education": info["education"],
            "experience_years": info["experience_years"],
            "experience_summary": info["experience_summary"],
            "all_skills": skills_data["all_skills"],
            "skills_by_category": skills_data["skills_by_category"],
            "raw_text": extracted_text,
            "cleaned_text": cleaned
        }
        
        cand_id = save_candidate(cand_dict)
        saved = get_candidate(cand_id)
        created_candidates.append(saved)
        
    return {
        "uploaded_count": len(created_candidates),
        "candidates": created_candidates,
        "errors": errors
    }

@app.get("/api/candidates")
def list_candidates():
    """Returns list of all uploaded candidates."""
    candidates = get_all_candidates()
    return {"count": len(candidates), "candidates": candidates}

@app.get("/api/candidates/{candidate_id}")
def get_candidate_detail(candidate_id: int):
    """Returns detailed profile for a specific candidate."""
    cand = get_candidate(candidate_id)
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return cand

@app.get("/api/resumes/download/{candidate_id}")
def download_resume(candidate_id: int):
    """Allows downloading the original resume file."""
    cand = get_candidate(candidate_id)
    if not cand or not os.path.exists(cand["file_path"]):
        raise HTTPException(status_code=404, detail="Resume file not found")
    return FileResponse(
        path=cand["file_path"],
        filename=cand["filename"],
        media_type="application/octet-stream"
    )

@app.post("/api/analyze")
def analyze_candidates(payload: AnalyzeRequest):
    """
    Analyzes candidates against a Job Description:
    - Calculates Skill Match %, Missing Skills, Additional Skills
    - Calculates TF-IDF Text Cosine Similarity
    - Computes Experience Score & Weighted Final Score
    - Saves results and returns ranked leaderboard
    """
    jd_id = payload.jd_id
    if not jd_id:
        latest_jd = get_latest_job_description()
        if not latest_jd:
            raise HTTPException(status_code=400, detail="No active Job Description found. Please submit a JD first.")
        jd = latest_jd
    else:
        jd = get_job_description(jd_id)
        if not jd:
            raise HTTPException(status_code=404, detail=f"Job Description {jd_id} not found")

    # Determine candidates to analyze
    if payload.candidate_ids:
        candidates = [get_candidate(cid) for cid in payload.candidate_ids if get_candidate(cid)]
    else:
        candidates = get_all_candidates()
        
    if not candidates:
        raise HTTPException(status_code=400, detail="No candidates found to analyze. Please upload resumes first.")

    weights = payload.weights.dict() if payload.weights else DEFAULT_WEIGHTS

    results = []
    for cand in candidates:
        match_result = match_candidate_to_jd(
            candidate_skills=cand["all_skills"],
            resume_cleaned_text=cand["cleaned_text"],
            candidate_experience_years=cand["experience_years"],
            jd_required_skills=jd["required_skills"],
            jd_cleaned_text=jd["description"],
            jd_min_experience_years=jd["min_experience_years"],
            weights=weights
        )
        
        save_match_result(
            candidate_id=cand["id"],
            jd_id=jd["id"],
            match_data=match_result
        )
        
    rankings = get_rankings_for_jd(jd["id"])
    return {
        "job_description_id": jd["id"],
        "job_title": jd["title"],
        "candidate_count": len(rankings),
        "rankings": rankings
    }

@app.get("/api/rankings")
def get_rankings(jd_id: Optional[int] = None):
    """Fetches candidate rankings for the given JD or latest JD."""
    target_jd = get_job_description(jd_id) if jd_id else get_latest_job_description()
    if not target_jd:
        return {"job_description": None, "rankings": []}
        
    rankings = get_rankings_for_jd(target_jd["id"])
    return {
        "job_description": target_jd,
        "rankings": rankings
    }

@app.post("/api/load-samples")
def load_sample_dataset():
    """
    One-click setup endpoint:
    1. Loads the Senior AI/ML Engineer sample JD.
    2. Ingests all 5 generated sample resumes (Rahul, Priya, Amit, Michael, Sneha).
    3. Analyzes and ranks them automatically.
    """
    # 1. Clear existing data
    clear_all_data()
    
    # 2. Insert AI/ML JD
    sample_jd_template = SAMPLE_JOB_DESCRIPTIONS[0]
    cleaned_desc = clean_text(sample_jd_template["description"])
    extracted = extract_jd_skills(cleaned_desc)
    
    jd_id = save_job_description(
        title=sample_jd_template["title"],
        description=cleaned_desc,
        required_skills=extracted["required_skills"],
        optional_skills=extracted["optional_skills"],
        keywords=extracted["all_skills"],
        min_experience_years=sample_jd_template["min_experience_years"]
    )
    saved_jd = get_job_description(jd_id)
    
    # 3. Ingest sample files
    sample_files = list(SAMPLE_RESUME_DIR.glob("*.pdf")) + list(SAMPLE_RESUME_DIR.glob("*.docx"))
    # Pick one file per candidate (mix of PDF and DOCX)
    selected_files = [
        SAMPLE_RESUME_DIR / "Rahul_Sharma_Senior_ML_Engineer.pdf",
        SAMPLE_RESUME_DIR / "Priya_Patel_FullStack_Engineer.docx",
        SAMPLE_RESUME_DIR / "Amit_Verma_Backend_Developer.pdf",
        SAMPLE_RESUME_DIR / "Michael_Chang_DevOps_Cloud_Architect.docx",
        SAMPLE_RESUME_DIR / "Sneha_Rao_Junior_Frontend_Developer.pdf"
    ]
    
    saved_candidates = []
    for s_file in selected_files:
        if not s_file.exists():
            continue
            
        ext = s_file.suffix.lower()
        if ext == ".pdf":
            raw_text = extract_text_from_pdf(s_file)
        else:
            raw_text = extract_text_from_docx(s_file)
            
        cleaned = clean_text(raw_text)
        info = extract_candidate_info(cleaned, filename=s_file.name)
        skills_data = extract_skills(cleaned)
        
        # Copy to uploads
        dest_path = UPLOAD_DIR / s_file.name
        shutil.copyfile(s_file, dest_path)
        
        cand_id = save_candidate({
            "filename": s_file.name,
            "file_type": ext.lstrip("."),
            "file_path": str(dest_path),
            "name": info["name"],
            "email": info["email"],
            "phone": info["phone"],
            "education": info["education"],
            "experience_years": info["experience_years"],
            "experience_summary": info["experience_summary"],
            "all_skills": skills_data["all_skills"],
            "skills_by_category": skills_data["skills_by_category"],
            "raw_text": raw_text,
            "cleaned_text": cleaned
        })
        saved_candidates.append(get_candidate(cand_id))
        
    # 4. Analyze against the JD
    for cand in saved_candidates:
        match_result = match_candidate_to_jd(
            candidate_skills=cand["all_skills"],
            resume_cleaned_text=cand["cleaned_text"],
            candidate_experience_years=cand["experience_years"],
            jd_required_skills=saved_jd["required_skills"],
            jd_cleaned_text=saved_jd["description"],
            jd_min_experience_years=saved_jd["min_experience_years"],
            weights=DEFAULT_WEIGHTS
        )
        save_match_result(
            candidate_id=cand["id"],
            jd_id=saved_jd["id"],
            match_data=match_result
        )
        
    rankings = get_rankings_for_jd(saved_jd["id"])
    return {
        "message": "Sample dataset loaded and analyzed successfully!",
        "job_description": saved_jd,
        "candidate_count": len(saved_candidates),
        "rankings": rankings
    }

@app.post("/api/clear")
def reset_system():
    """Clears all candidates, match results, and JDs."""
    clear_all_data()
    return {"message": "All database records have been reset successfully."}
