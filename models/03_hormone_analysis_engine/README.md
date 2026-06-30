# Oviora Hormone Intelligence

Oviora Hormone Intelligence is a production-grade, AI-assisted clinical decision-support API designed for analyzing laboratory blood reports (such as hormone panels relevant to PCOS, thyroid function, and metabolic health).

It extracts medical biomarkers from PDF reports or images via OCR, validates and normalizes them, and leverages Large Language Models (LLMs) with multi-provider fallbacks to produce comprehensive, structured summaries, follow-up recommendations, and doctor discussion guides.

---

## Key Features

- **Document Ingestion**: Supports uploading PDF reports and image formats (`.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`).
- **OCR Engine**: Utilizes PaddleOCR 3.x with unwarping and textline orientation classifiers.
- **Biomarker Normalization**: Parses arbitrary laboratory findings, matches them to an internal medical ontology alias database, and standardizes units.
- **Reference Range Validation**: Identifies biomarker abnormalities (`normal`, `high`, `low`) against standard clinical reference ranges.
- **Multi-tiered LLM Orchestrator**:
  - **Primary**: Google Gemini 2.5 Flash.
  - **Secondary Fallback**: Groq (Llama-3.3-70b-versatile).
  - **Tertiary Fallback**: Local deterministic rule engine (runs completely offline if LLM providers are unavailable).
- **Multi-Format Export**: Generates report analyses in **JSON**, **Markdown**, **HTML**, and **PDF** formats.
- **API Framework**: Built on FastAPI with automatic OpenAPI interactive documentation (`/docs`).

---

## Directory Structure

```text
├── app/
│   ├── api/                  # FastAPI router endpoints (upload, analyze, reports, health)
│   ├── data/                 # Biomarker medical ontology mapping & reference ranges
│   │   ├── ontology/
│   │   └── reference_ranges/
│   ├── services/             # Core pipelines (OCR, parsing, rule engine, LLM, formatting)
│   ├── config.py             # Pydantic environment configuration settings
│   ├── logger.py             # Standardized application logger
│   └── main.py               # FastAPI server instance initiation
├── tests/                    # 48 automated unit and integration tests
├── uploads/                  # Temporary storage directory for uploaded reports
├── reports/                  # Export directory for processed JSON, MD, HTML, and PDF reports
├── .env                      # Local environment configuration settings
├── requirements.txt          # Python dependencies list
├── run_integration_test.py   # Automated end-to-end pipeline test script
└── test_user_report.py       # Injectable parser/analyzer test runner for ZRT reports
```

---

## Local Setup

### 1. Prerequisites
- Python 3.10 to 3.13
- System-level dependencies for PDF rendering and OCR:
  - macOS: `brew install poppler`
  - Ubuntu/Linux: `sudo apt-get install poppler-utils`

### 2. Create Virtual Environment & Install Dependencies
```bash
# Initialize virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root folder (using `env.example` as a template):
```env
# Application Settings
APP_NAME=Oviora Hormone Intelligence
VERSION=1.0.0
DEBUG=False
PORT=8000

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Groq API
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## Testing & Verification

### A. Run Automated Unit Tests
Run the entire suite of 48 unit and integration tests:
```bash
.venv/bin/python -m pytest
```

### B. Run End-to-End Pipeline Integration Test
This spins up a background FastAPI server, generates a mock hormone lab report, uploads it, triggers OCR, and runs the entire analysis:
```bash
.venv/bin/python run_integration_test.py
```

### C. Run Specific Laboratory Report Test
Test the system's parsing and analysis against the text of a real **ZRT Laboratory Hormone Report**:
```bash
.venv/bin/python test_user_report.py
```

---

## Production Deployment

### 1. Launch FastAPI Server
Start the local server instance on port 8000:
```bash
.venv/bin/python -m uvicorn app.main:app --port 8000 --reload
```
Once active, visit **`http://localhost:8000/docs`** to interact with the API Swagger UI.

### 2. Primary API Endpoints

#### `POST /upload`
Uploads a lab report document.
- **Request**: Multipart Form Data (`file: UploadFile`).
- **Response (201)**:
  ```json
  {
    "success": true,
    "message": "File uploaded successfully.",
    "file_id": "a1b2c3d4e5f6.png"
  }
  ```

#### `POST /analyze/{file_id}`
Triggers the full processing and clinical report generation pipeline.
- **Request**: Path Parameter `file_id`.
- **Response (200)**:
  ```json
  {
    "success": true,
    "provider": "gemini",
    "report": {
      "executive_summary": "Analysis generated using gemini. Overall confidence score: 0.995.",
      "biomarkers": [ ... ],
      "assessments": { "hormonal": [ ... ], "thyroid": [ ... ] },
      "derived_metrics": { "LH_FSH_Ratio": 0.67 }
    },
    "downloads": {
      "pdf": "/reports/a1b2c3d4e5f6.pdf",
      "html": "/reports/a1b2c3d4e5f6.html"
    }
  }
  ```

#### `GET /reports`
Lists all generated reports saved on the server.

#### `GET /health`
Returns system liveness status and software version.

---

## Medical Compliance Boundaries

Oviora is strictly a decision-support prototype. The internal prompts and rule systems strictly adhere to the following guardrails:
1. **No Diagnosis**: Never diagnoses conditions (e.g., PCOS, Hypothyroidism) directly. Instead, it flags biomarker deviations (e.g., "TSH is elevated").
2. **No Treatment Plans**: Never prescribes medications, supplements, dosages, or lifestyle changes.
3. **No Biomarker Creation**: Only reviews tests present in the provided report; missing parameters are documented explicitly.
