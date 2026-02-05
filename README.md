# Exercise Starter - Results Upload (Take-Home)

## Overview
- This starter app reduces setup time so candidates can focus on the problem.
- Stack: Vue 3 + TypeScript (Vite), Tailwind; FastAPI (Python 3.12), Pydantic v2; SQLAlchemy 2.x.
- Data: CSV upload with light validation and summary reporting.

## Take-Home (2-3 hrs)
- Expectation: complete end-to-end flow with small but real tests on both FE/BE; SQLite or in-memory OK.

## What To Build
- Backend
  - POST `/api/results/upload` accepts a CSV with headers: `id,status,ts,notes` (scaffolding exists already).
  - Validate rows (required headers; id non-empty; status in success|fail|unknown; ts ISO8601), dedupe by `(id, ts)` keeping the first.
  - Persist to a temp table (SQLite acceptable for exercise) or in-memory store.
  - Respond with JSON summary: `{ total_rows, valid_rows, errors:[{row, reason}], by_status:{success, fail, unknown} }`.
- Frontend
  - Frontend page with drag-and-drop file input, upload progress, and a summary view (table and a simple chart optional).
  - Drag-and-drop or file picker, upload progress/feedback, render summary.

## Acceptance Criteria
- Backend: FastAPI route, request validation, CSV parsing with streaming or chunking (no full file in memory for large files), deduplication, structured JSON response, and basic tests (pytest) for happy path + 1-2 errors.
- Frontend: Vue page/component, async upload with progress feedback, render summary and error count; basic unit test(s) with Vitest.
- DX: Clear README/run steps; sensible project structure; linters passing or minimal warnings.
- Please include: how you'd harden this for production (1-2 paragraphs: retries, chunked uploads, S3 presigned URLs, idempotency, Celery for heavy processing, Postgres partitioning/indexing, observability).

## Deliverables
- Github repo or zip with `frontend/` and `backend/`
- Markdown file with your ideas for how you'd harden this feature for production.

## Submission
- Share a GitHub link or zip via email. Please do not include proprietary work.

# App setup
Prereqs
- Python 3.12
- Node.js 20

## Backend (FastAPI)
1) Setup
   - `cd backend`
   - `python -m venv .venv && . .venv/Scripts/activate` (Windows) or `. .venv/bin/activate` (macOS/Linux)
   - `pip install -r requirements.txt`
2) Run
   - `uvicorn app.main:app --reload --port 8000`
   - Health check: use Swagger or curl:
     - `curl -X POST -F "file=@docs/hiring/exercise-starter/sample.csv" http://localhost:8000/api/results/upload`
   - Swagger generated documentation available at `http://localhost:8000/docs`
3) Test
   - `pytest -q`

## Frontend (Vue 3 + Vite)
1) Setup
   - `cd frontend`
   - `npm install`
2) Run
   - `npm run dev` then open the URL (default `http://localhost:5173`)
   - API defaults to `http://localhost:8000/api` (override with `VITE_API_URL`)
3) Test
   - `npm run test`

## Sample Data
- See `sample.csv`
