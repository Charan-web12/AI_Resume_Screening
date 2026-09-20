# TalentPulse AI: AI Resume Screening & Candidate Matching System

> A production-grade, explainable, AI-assisted recruitment platform that automatically parses resumes (PDF & DOCX), normalizes technical skills, performs TF-IDF cosine semantic matching and skill-gap analysis against target Job Descriptions, and ranks candidates with a modern recruiter dashboard.

---

## 🌟 Key Features

1. **Multi-Format Resume Ingestion**:
   - Accepts batch uploads of resumes in both **PDF** and **DOCX** formats.
   - Robust document extractors using `pypdf` and `python-docx` with character normalization, bullet symbol cleanup, and section segmenting.
   - Graceful validation and error handling for corrupt or unsupported file formats.

2. **NLP-Based Skill Extraction & Normalization**:
   - Curated taxonomy of **400+ technical skills** spanning Languages, Frontend, Backend, Databases, Cloud & DevOps, AI/ML/Data Science, and Tools.
   - Intelligent alias mapping (e.g., `Python 3` / `Python Programming` $\rightarrow$ `Python`, `ReactJS` $\rightarrow$ `React`, `Amazon Web Services` $\rightarrow$ `AWS`, `K8s` $\rightarrow$ `Kubernetes`, `Postgres` $\rightarrow$ `PostgreSQL`).
   - Boundary-safe extraction distinguishing single-letter/short technologies (`R`, `Go`, `C++`, `C#`, `.NET`) from ordinary text.

3. **Candidate Profile Extraction**:
   - Automated identification of Candidate Name, Email, Phone Number, Education degrees, and Experience tenure.
   - Generates candidate experience summaries and categorizes skills by technical domain.

4. **Explainable AI Matching Engine**:
   - **TF-IDF + Cosine Similarity**: Employs `scikit-learn` `TfidfVectorizer` (unigrams & bigrams with stop-words) to evaluate full-text semantic overlap.
   - **Skill Coverage Analysis**: Accurately computes `Matched Skills`, `Missing Skills`, and `Additional Skills` (skills candidate possesses beyond the JD).
   - **Experience Qualification**: Compares candidate detected tenure against role seniority requirements.
   - **Weighted Scoring Formula**:
     $$\text{Final Score} = (w_{\text{skill}} \times \text{SkillScore}) + (w_{\text{text}} \times \text{TextSimScore}) + (w_{\text{exp}} \times \text{ExpScore})$$
     *(Default: 60% Skill Match, 30% TF-IDF Text Similarity, 10% Experience Qualification — fully tunable via the UI).*
   - **Complete Explainability**: Explicit breakdown displaying exact mathematical points, formulas, and narrative reasoning.

5. **Recruiter SaaS Dashboard**:
   - **Job Description Studio**: Pre-packaged JD templates (Senior AI/ML, Full-Stack, Lead DevOps) + custom JD input with auto-skill extraction.
   - **Rankings Leaderboard**: Gold, Silver, and Bronze rank badges; score tier filtering (High $\ge 75\%$, Moderate $55-74\%$, Low $<55\%$); search by candidate name or specific skill (e.g., "Docker", "PyTorch").
   - **Candidate Deep-Dive Profile**: Modal displaying contact info, education, categorized skills matrix, raw text viewer, and recruiter decision actions (Shortlist/Reject).
   - **Side-by-Side Comparison Matrix**: Compare up to 3 candidates simultaneously across all required competencies.
   - **One-Click Sample Suite**: Pre-loaded with 5 diverse candidates and realistic resumes for instant demonstration.

6. **Ethical AI & Compliance**:
   - Strictly evaluates technical competencies, experience tenure, and job description semantic overlap.
   - Demographic characteristics (gender, race, age, religion, nationality) are omitted from scoring.
   - Prominent AI assistance disclosure banner stating that hiring decisions remain with human recruiters.

---

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, Uvicorn, SQLite
- **NLP / ML**: `scikit-learn` (TF-IDF Vectorizer, Cosine Similarity), `numpy`, `scipy`
- **Document Processing**: `pypdf`, `python-docx`, `reportlab`
- **Frontend**: React.js, Vite, Vanilla CSS Design System, `lucide-react` icons
- **Testing**: `pytest`, FastAPI TestClient

---

## 📂 Project Structure

```
AI_resume_screening/
├── backend/
│   ├── database/
│   │   ├── db.py                 # SQLite database schema, connections, queries
│   │   └── __init__.py
│   ├── parsers/
│   │   ├── cleaner.py            # Text cleaning & unicode normalization
│   │   ├── pdf_parser.py         # PyPDF text extraction
│   │   ├── docx_parser.py        # Python-docx paragraphs & tables extraction
│   │   └── __init__.py
│   ├── nlp/
│   │   ├── taxonomy.py           # 400+ skill taxonomy & alias mapping
│   │   ├── skill_extractor.py    # Skill extraction & JD analyzer
│   │   ├── info_extractor.py     # Name, contact, education, experience extraction
│   │   ├── matcher.py            # TF-IDF cosine similarity & scoring engine
│   │   └── __init__.py
│   ├── data/
│   │   ├── sample_jds.py         # Sample Job Description templates
│   │   └── sample_resumes/       # 5 realistic resumes (PDF & DOCX)
│   ├── scripts/
│   │   └── generate_sample_resumes.py # Script to generate test resumes
│   ├── tests/
│   │   ├── test_parsers.py       # Unit tests for PDF & DOCX parsing
│   │   ├── test_nlp.py           # Unit tests for skill & info extraction
│   │   ├── test_matcher.py       # Unit tests for TF-IDF & explainable matching
│   │   └── test_api.py           # Integration tests for FastAPI endpoints
│   ├── main.py                   # FastAPI application & REST endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── EthicalDisclaimer.jsx
│   │   │   ├── MetricsOverview.jsx
│   │   │   ├── JobDescriptionSection.jsx
│   │   │   ├── ResumeUploadSection.jsx
│   │   │   ├── RankingsLeaderboard.jsx
│   │   │   ├── CandidateDetailModal.jsx
│   │   │   ├── CandidateCompareModal.jsx
│   │   │   └── WeightsModal.jsx
│   │   ├── api.js                # Frontend API client
│   │   ├── App.jsx               # Main dashboard orchestrator
│   │   ├── main.jsx
│   │   └── index.css             # Glassmorphism dark SaaS design tokens
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# In the root directory:
python -m pip install -r requirements.txt

# Run automated tests to verify setup:
python -m pytest backend/tests

# Start the FastAPI server on port 8000:
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
The backend will be live at `http://127.0.0.1:8000` (API docs at `http://127.0.0.1:8000/docs`).

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The React recruiter dashboard will be live at `http://localhost:5173`.

---

## 🎯 Testing the Application in 1 Click

1. Open `http://localhost:5173` in your browser.
2. Click the **"⚡ Load Sample Suite"** button in the top navbar.
3. The platform will automatically:
   - Ingest the **Senior AI & Machine Learning Engineer** Job Description.
   - Parse all 5 realistic applicant resumes (Rahul Sharma, Priya Patel, Amit Verma, Michael Chang, Sneha Rao) in both PDF and DOCX.
   - Run the TF-IDF cosine matching and skill gap pipeline.
   - Display the ranked leaderboard with instant match percentages, matched vs missing skills, and detailed analytics!

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Health check endpoint |
| `/api/job-description/templates` | `GET` | Get sample JD templates |
| `/api/job-description/latest` | `GET` | Get currently active JD |
| `/api/job-description` | `POST` | Submit a JD (auto-extracts required & bonus skills) |
| `/api/resumes/upload` | `POST` | Upload multiple resumes (PDF / DOCX) |
| `/api/candidates` | `GET` | List all uploaded candidates |
| `/api/candidates/{id}` | `GET` | Get detailed candidate profile and extracted skills |
| `/api/resumes/download/{id}` | `GET` | Download or view the candidate's original resume file |
| `/api/analyze` | `POST` | Execute matching analysis against JD with custom weights |
| `/api/rankings` | `GET` | Retrieve ranked candidates for active JD |
| `/api/load-samples` | `POST` | One-click setup: populates sample JD and 5 sample candidates |
| `/api/clear` | `POST` | Reset all database entries |
#   A I _ R e s u m e _ S c r e e n i n g  
 