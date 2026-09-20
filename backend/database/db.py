import sqlite3
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_DIR = Path(__file__).resolve().parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "screening.db"

_db_initialized = False

def get_connection() -> sqlite3.Connection:
    global _db_initialized
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    if not _db_initialized:
        init_db(conn)
        _db_initialized = True
    return conn

def init_db(existing_conn: Optional[sqlite3.Connection] = None):
    should_close = existing_conn is None
    conn = existing_conn or sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_descriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        required_skills TEXT DEFAULT '[]',
        optional_skills TEXT DEFAULT '[]',
        keywords TEXT DEFAULT '[]',
        min_experience_years REAL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        name TEXT DEFAULT 'Unknown Candidate',
        email TEXT DEFAULT '',
        phone TEXT DEFAULT '',
        education TEXT DEFAULT '[]',
        experience_years REAL DEFAULT 0,
        experience_summary TEXT DEFAULT '',
        all_skills TEXT DEFAULT '[]',
        skills_by_category TEXT DEFAULT '{}',
        raw_text TEXT NOT NULL,
        cleaned_text TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        job_description_id INTEGER NOT NULL,
        overall_score REAL NOT NULL,
        skill_score REAL NOT NULL,
        text_similarity_score REAL NOT NULL,
        experience_score REAL NOT NULL,
        matched_skills TEXT DEFAULT '[]',
        missing_skills TEXT DEFAULT '[]',
        additional_skills TEXT DEFAULT '[]',
        explanation TEXT DEFAULT '{}',
        created_at TEXT NOT NULL,
        FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
        FOREIGN KEY (job_description_id) REFERENCES job_descriptions(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    if should_close:
        conn.close()

# Helper access functions
def save_job_description(title: str, description: str, required_skills: List[str], 
                         optional_skills: List[str] = None, keywords: List[str] = None, 
                         min_experience_years: float = 0.0) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO job_descriptions (title, description, required_skills, optional_skills, keywords, min_experience_years, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        json.dumps(required_skills),
        json.dumps(optional_skills or []),
        json.dumps(keywords or []),
        min_experience_years,
        now
    ))
    jd_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jd_id

def get_job_description(jd_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions WHERE id = ?", (jd_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "required_skills": json.loads(row["required_skills"]),
        "optional_skills": json.loads(row["optional_skills"]),
        "keywords": json.loads(row["keywords"]),
        "min_experience_years": row["min_experience_years"],
        "created_at": row["created_at"]
    }

def get_latest_job_description() -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "required_skills": json.loads(row["required_skills"]),
        "optional_skills": json.loads(row["optional_skills"]),
        "keywords": json.loads(row["keywords"]),
        "min_experience_years": row["min_experience_years"],
        "created_at": row["created_at"]
    }

def save_candidate(candidate_data: Dict[str, Any]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO candidates (
            filename, file_type, file_path, name, email, phone, 
            education, experience_years, experience_summary, 
            all_skills, skills_by_category, raw_text, cleaned_text, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_data.get("filename", "unknown"),
        candidate_data.get("file_type", "pdf"),
        candidate_data.get("file_path", ""),
        candidate_data.get("name", "Unknown"),
        candidate_data.get("email", ""),
        candidate_data.get("phone", ""),
        json.dumps(candidate_data.get("education", [])),
        candidate_data.get("experience_years", 0),
        candidate_data.get("experience_summary", ""),
        json.dumps(candidate_data.get("all_skills", [])),
        json.dumps(candidate_data.get("skills_by_category", {})),
        candidate_data.get("raw_text", ""),
        candidate_data.get("cleaned_text", ""),
        now
    ))
    cand_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return cand_id

def get_candidate(candidate_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row["id"],
        "filename": row["filename"],
        "file_type": row["file_type"],
        "file_path": row["file_path"],
        "name": row["name"],
        "email": row["email"],
        "phone": row["phone"],
        "education": json.loads(row["education"]),
        "experience_years": row["experience_years"],
        "experience_summary": row["experience_summary"],
        "all_skills": json.loads(row["all_skills"]),
        "skills_by_category": json.loads(row["skills_by_category"]),
        "raw_text": row["raw_text"],
        "cleaned_text": row["cleaned_text"],
        "created_at": row["created_at"]
    }

def get_all_candidates() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "filename": row["filename"],
            "file_type": row["file_type"],
            "file_path": row["file_path"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "education": json.loads(row["education"]),
            "experience_years": row["experience_years"],
            "experience_summary": row["experience_summary"],
            "all_skills": json.loads(row["all_skills"]),
            "skills_by_category": json.loads(row["skills_by_category"]),
            "raw_text": row["raw_text"],
            "cleaned_text": row["cleaned_text"],
            "created_at": row["created_at"]
        })
    return result

def save_match_result(candidate_id: int, jd_id: int, match_data: Dict[str, Any]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    # Delete existing match for same pair if re-analyzed
    cursor.execute("DELETE FROM match_results WHERE candidate_id = ? AND job_description_id = ?", (candidate_id, jd_id))
    cursor.execute("""
        INSERT INTO match_results (
            candidate_id, job_description_id, overall_score, skill_score, 
            text_similarity_score, experience_score, matched_skills, 
            missing_skills, additional_skills, explanation, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_id,
        jd_id,
        match_data.get("overall_score", 0.0),
        match_data.get("skill_score", 0.0),
        match_data.get("text_similarity_score", 0.0),
        match_data.get("experience_score", 0.0),
        json.dumps(match_data.get("matched_skills", [])),
        json.dumps(match_data.get("missing_skills", [])),
        json.dumps(match_data.get("additional_skills", [])),
        json.dumps(match_data.get("explanation", {})),
        now
    ))
    match_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return match_id

def get_rankings_for_jd(jd_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            m.*, 
            c.name as candidate_name,
            c.filename,
            c.file_type,
            c.email,
            c.phone,
            c.education,
            c.experience_years,
            c.experience_summary,
            c.all_skills
        FROM match_results m
        JOIN candidates c ON m.candidate_id = c.id
        WHERE m.job_description_id = ?
        ORDER BY m.overall_score DESC
    """, (jd_id,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for rank, row in enumerate(rows, 1):
        results.append({
            "rank": rank,
            "match_id": row["id"],
            "candidate_id": row["candidate_id"],
            "job_description_id": row["job_description_id"],
            "candidate_name": row["candidate_name"],
            "filename": row["filename"],
            "file_type": row["file_type"],
            "email": row["email"],
            "phone": row["phone"],
            "education": json.loads(row["education"]),
            "experience_years": row["experience_years"],
            "experience_summary": row["experience_summary"],
            "all_skills": json.loads(row["all_skills"]),
            "overall_score": row["overall_score"],
            "skill_score": row["skill_score"],
            "text_similarity_score": row["text_similarity_score"],
            "experience_score": row["experience_score"],
            "matched_skills": json.loads(row["matched_skills"]),
            "missing_skills": json.loads(row["missing_skills"]),
            "additional_skills": json.loads(row["additional_skills"]),
            "explanation": json.loads(row["explanation"]),
            "created_at": row["created_at"]
        })
    return results

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM match_results")
    cursor.execute("DELETE FROM candidates")
    cursor.execute("DELETE FROM job_descriptions")
    conn.commit()
    conn.close()

def delete_candidate(candidate_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    file_path = row["file_path"]
    cursor.execute("DELETE FROM match_results WHERE candidate_id = ?", (candidate_id,))
    cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()
    conn.close()

    if file_path and os.path.exists(file_path):
        try:
            # Only remove if inside uploads folder
            if "uploads" in str(file_path):
                os.remove(file_path)
        except OSError:
            pass
    return True

def clear_candidates() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM candidates")
    rows = cursor.fetchall()
    cursor.execute("DELETE FROM match_results")
    cursor.execute("DELETE FROM candidates")
    conn.commit()
    conn.close()

    deleted_count = len(rows)
    for row in rows:
        f_path = row["file_path"]
        if f_path and os.path.exists(f_path):
            try:
                if "uploads" in str(f_path):
                    os.remove(f_path)
            except OSError:
                pass
    return deleted_count

