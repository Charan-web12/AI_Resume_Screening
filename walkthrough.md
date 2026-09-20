# AI Resume Screening & Candidate Matching System - Walkthrough

We have designed, built, and verified the complete full-stack **AI Resume Screening & Candidate Matching System** (TalentPulse AI).

---

## 🎯 What Was Built

### 1. Robust Multi-Format Document Parsers (`backend/parsers/`)
- **PDF Parser (`pdf_parser.py`)**: Reads multi-column, multi-page resumes using `pypdf.PdfReader` with stream and path support.
- **DOCX Parser (`docx_parser.py`)**: Extracts text from paragraphs, tables, and bulleted lists using `python-docx`.
- **Text Cleaner (`cleaner.py`)**: Normalizes Unicode, cleans bullet characters (`•`, `▪`, `✓`, `\x7f`), collapses repeated spaces, and formats clean text blocks.

### 2. Comprehensive NLP & Skill Extraction Engine (`backend/nlp/`)
- **Curated Skill Taxonomy (`taxonomy.py`)**: Curated database of **400+ technical skills** grouped into 7 domains:
  - *Programming Languages*, *Frontend*, *Backend*, *Databases*, *Cloud & DevOps*, *AI/ML/Data Science*, *Tools & Engineering*.
- **Alias Normalization (`skill_extractor.py`)**: Maps variations to canonical names (e.g. `Python 3` / `Python Programming` $\rightarrow$ `Python`, `ReactJS` $\rightarrow$ `React`, `Amazon Web Services` $\rightarrow$ `AWS`, `K8s` $\rightarrow$ `Kubernetes`, `Postgres` $\rightarrow$ `PostgreSQL`).
- **Boundary-Safe Extraction**: Accurately recognizes short technologies (`R`, `Go`, `C++`, `C#`, `.NET`) with lookarounds to prevent false positives.
- **Candidate Profile Extractor (`info_extractor.py`)**: Extracts Candidate Name, Email, Phone, Education degrees, and Experience tenure.

### 3. Explainable Matching & Ranking Engine (`backend/nlp/matcher.py`)
- **TF-IDF + Cosine Similarity**: Employs `scikit-learn` `TfidfVectorizer` (unigram/bigram features with English stop-words) and cosine similarity to evaluate semantic content overlap.
- **Skill Gap Analysis**: Computes `Matched Skills`, `Missing Skills`, and `Additional Skills`.
- **Experience Qualification**: Evaluates candidate experience years against role seniority requirements.
- **Weighted Scoring**:
  $$\text{Final Score} = (w_{\text{skill}} \times \text{SkillScore}) + (w_{\text{text}} \times \text{TextSimScore}) + (w_{\text{exp}} \times \text{ExpScore})$$
  *(Default: 60% Skill Match, 30% Text Similarity, 10% Experience Qualification).*
- **Explainability**: Generates point contributions, breakdown percentages, and narrative reasoning.

### 4. SQLite Persistence & REST APIs (`backend/database/` & `backend/main.py`)
- **Tables**: `job_descriptions`, `candidates`, `match_results`.
- **Endpoints**:
  - `POST /api/job-description`: Parses JD and extracts required vs bonus skills.
  - `POST /api/resumes/upload`: Uploads and parses multiple PDF/DOCX resumes.
  - `POST /api/analyze`: Executes matching and generates rankings.
  - `GET /api/rankings`: Returns sorted candidate rankings.
  - `GET /api/candidates/{id}`: Detailed candidate profile and skills breakdown.
  - `GET /api/resumes/download/{id}`: Original resume download.
  - `POST /api/load-samples`: 1-click test suite populating 5 candidates and JD.
  - `POST /api/clear`: Resets database.

### 5. Modern Recruiter Dashboard (`frontend/`)
- **SaaS Dark Design**: Custom CSS tokens, glassmorphism (`backdrop-filter: blur(14px)`), Google Fonts (`Outfit` + `Inter`), and `lucide-react` icons.
- **Ethical AI Disclaimer**: Explains the AI-assisted nature of the system and non-use of protected characteristics.
- **Metric Cards**: Total Resumes, Screened & Ranked, High Match Count, and Average Match Score.
- **Job Description Studio**: Template buttons (Senior AI/ML, Full Stack, DevOps) and custom JD input.
- **Resume Ingestion Zone**: Drag-and-drop file dropzone with PDF/DOCX format validation.
- **Leaderboard**: Rank badges (#1 Gold, #2 Silver, #3 Bronze), score progress bars, matched/missing skill pills, search by name/skill, and tier filtering.
- **Candidate Profile Modal**: Deep-dive profile with contact info, education, explainable formula breakdown, categorized skills matrix, and raw text toggle.
- **Candidate Comparison Matrix**: Side-by-side comparison of multiple candidates across all required competencies.
- **Scoring Weights Tuner Modal**: Sliders to customize matching weights in real time.

---

## 🧪 Verification & Test Results

### 1. Automated Unit & Integration Tests
Ran `pytest backend/tests`:
```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
collected 11 items

backend\tests\test_api.py ...                                            [ 27%]
backend\tests\test_matcher.py ..                                         [ 45%]
backend\tests\test_nlp.py ...                                            [ 72%]
backend\tests\test_parsers.py ...                                        [100%]

======================= 11 passed in 2.26s ========================
```
- **Parsers**: PDF and DOCX file extraction validated.
- **NLP**: Skill normalization, alias mapping, and candidate info extraction validated.
- **Matcher**: TF-IDF cosine similarity, skill overlap, and scoring formula validated.
- **API**: `/api/health`, `/api/load-samples`, `/api/rankings`, and `/api/job-description` validated.

### 2. Frontend Production Build
Ran `npm run build`:
```
✓ 1888 modules transformed.
dist/index.html                   0.99 kB │ gzip:  0.53 kB
dist/assets/index-BgSoTqZH.css   10.92 kB │ gzip:  2.83 kB
dist/assets/index-CUqNq7H5.js   275.51 kB │ gzip: 81.92 kB
✓ built in 1.04s
```

### 3. End-to-End Live HTTP & Proxy Verification
Tested both the backend (`http://127.0.0.1:8000`) and the frontend dev server (`http://localhost:5173`):
- `GET http://localhost:5173/` $\rightarrow$ `Status: 200 OK`
- `GET http://localhost:5173/api/health` $\rightarrow$ `Status: 200 {'status': 'ok', 'service': 'AI Resume Screening API'}`
- `POST http://127.0.0.1:8000/api/load-samples` $\rightarrow$ `Status: 200 (5 candidates parsed and analyzed)`
- `GET http://localhost:5173/api/rankings` $\rightarrow$ `Status: 200`
  - **Rank 1**: Rahul Sharma (**74.8%** - Senior ML Engineer, 27 skills detected, 19/20 required skills matched)
  - **Rank 2**: Priya Patel (**63.1%** - Full Stack Developer, 19 skills detected)
  - **Rank 3**: Michael Chang (**54.2%** - DevOps Engineer, 17 skills detected)
  - **Rank 4**: Amit Verma (**52.3%** - Backend Developer, 16 skills detected)
  - **Rank 5**: Sneha Rao (**36.8%** - Junior Frontend Developer, 10 skills detected)

---

## 💻 How to Run Locally

1. **Start the Backend**:
   ```bash
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```
3. Open `http://localhost:5173` in your web browser and click **"⚡ Load Sample Suite"** in the top navbar to explore the system!
