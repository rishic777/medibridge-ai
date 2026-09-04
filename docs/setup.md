# Setup

## Option A — Docker (fastest)

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (docs at `/docs`)
- Postgres: localhost:5432 (auto-seeded from `database/schema.sql` + `database/seed.sql`)

## Option B — Manual

### 1. Database

```bash
createdb medibridge
psql -d medibridge -f database/schema.sql
psql -d medibridge -f database/seed.sql   # optional demo data
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # edit DATABASE_URL / AI_PROVIDER / AI_API_KEY
uvicorn app.main:app --reload
```

The backend auto-creates tables on startup in dev mode, so step 1 is
optional if you just want to try the API — but `schema.sql` is the
canonical source of truth for production.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env              # set VITE_API_URL if backend isn't on :8000
npm run dev
```

Open http://localhost:5173.

## Switching the AI provider

Edit `backend/.env`:

```
AI_PROVIDER=gemini   # or "openai", or "local" (offline stub, default)
AI_API_KEY=your-real-key
AI_MODEL=gemini-1.5-flash
```

No code changes needed — see `backend/app/services/ai_providers.py`.

## Editing questions / red flags without touching code

- Interview questions: `config/questions/<condition>.json`
- Safety rules: `config/red_flags/rules.json`
- UI language strings: `config/languages/<lang>.json`

## Running tests

```bash
cd backend
pytest
```
