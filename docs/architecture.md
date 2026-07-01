# Oviora Platform Architecture

This document details the overarching system architecture for the Oviora platform. Oviora uses a decoupled client-server architecture with a React-based frontend and a Python-based backend designed for heavy machine learning inference.

---

## 1. High-Level System Architecture

The system is split into two primary monoliths:

1. **Frontend Client:** A Next.js (React) application responsible for UI rendering, state management, and user interactions.
2. **Backend Server:** A FastAPI (Python) application responsible for business logic, data persistence, and AI model inference.

```text
[ User Browser ] <--> [ Next.js Frontend ] <--> [ FastAPI Backend ]
                                                       |
                                            [ AI Inference Engines ]
```

---

## 2. Backend Architecture (FastAPI Monolith)

The backend is built as a modular monolith. It is organized by domain capabilities to ensure separation of concerns and allow for easy future microservice extraction if needed.

### Directory Structure
- `/backend/app`: The core application directory.
- `/backend/app/api/v1`: Contains the router endpoints (e.g., `/cycle/predict`, `/labs/upload`).
- `/backend/app/services`: Contains the business logic and AI model initialization. This is where models like the CatBoost risk engine and PaddleOCR are loaded into memory.
- `/backend/app/core`: Configuration management (e.g., `pydantic-settings` for environment variables).

### AI Model Integration
Models are loaded into memory at application startup (via FastAPI lifespan events or global instantiation in services) to ensure fast inference times. 
- **Cycle Engine:** Runs inference via scikit-learn/custom logic on incoming JSON payloads.
- **Lab Analyzer:** Receives multipart file uploads, temporarily stores or processes them in-memory, and passes them through the PaddleOCR pipeline.

### Configuration Strategy
Environment variables are strictly decoupled. The backend relies on a robust `pydantic-settings` configuration module, utilizing `.env` files for isolated environment setups.

---

## 3. Frontend Architecture (Next.js)

The frontend uses the modern Next.js App Router for optimized routing and layout management.

### Service Layer (`src/services/api.ts`)
The frontend communicates with the backend exclusively through a dedicated API service layer. This layer abstracts `fetch` calls, handles error fallbacks, and standardizes data contracts. Currently, it implements real backend integrations for:
- Cycle Intelligence
- Clinical Risk Prediction
- Lab Report OCR Uploads
*(Other features rely on mock data while backend development continues).*

### Authentication & Routing
The application utilizes an authenticated route group `(dashboard)` which wraps protected pages with a persistent Layout (Sidebar and Top Navigation).

---

## 4. Security & Data Flow

1. **API Contracts:** The frontend and backend communicate using strict JSON schemas defined via Pydantic on the backend and TypeScript interfaces on the frontend.
2. **CORS:** The FastAPI backend implements a CORS middleware to securely allow requests only from the frontend origin.
3. **Environment Isolation:** Sensitive keys and model configurations are never exposed to the client.
