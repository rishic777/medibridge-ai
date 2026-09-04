# Architecture

MediBridge AI is built as a layered, configuration-driven platform rather
than a single hard-coded app, so the same skeleton can be reused for a
different AI-assisted intake product later by swapping only the content
layers (questions, prompts, business rules, UI copy) — not the platform
itself.

## Layers

```
┌────────────────────────────────────────┐
│             PRESENTATION               │  React (frontend/)
├────────────────────────────────────────┤
│              API LAYER                 │  FastAPI routers (backend/app/api/)
├────────────────────────────────────────┤
│          APPLICATION LOGIC             │  backend/app/services/
├────────────────────────────────────────┤
│              AI LAYER                  │  AIProvider abstraction (ai_providers.py)
├────────────────────────────────────────┤
│             SAFETY LAYER               │  backend/app/safety/
├────────────────────────────────────────┤
│             DATA LAYER                 │  PostgreSQL (database/schema.sql)
├────────────────────────────────────────┤
│        EXTERNAL INTEGRATIONS           │  AI vendor, OCR, ASR
└────────────────────────────────────────┘
```

Each layer only talks to the one directly below it. The frontend never
calls an AI vendor or the database directly; it only calls the API layer.

## Key patterns

**AIProvider abstraction** (`backend/app/services/ai_providers.py`) — the
rest of the app calls `AIService`, never a vendor SDK directly. Switching
from Gemini to OpenAI (or a local model) means editing `AI_PROVIDER` in
`.env` and, if needed, one class in this file.

**Config-driven content** (`/config`) — interview questions
(`config/questions/*.json`), red-flag safety rules
(`config/red_flags/rules.json`), and UI copy per language
(`config/languages/*.json`) are all data, not code. A clinician or
product owner can edit these without a deploy.

**Three-layer verification** — every clinical fact carries a `source`:
`patient_reported` → `document_supported` → `physician_verified`. This is
enforced end to end: the `symptoms.source` column, the
`verification_records` audit table, the `VerificationBadge` component,
and the safety-language guardrails in `backend/app/safety/validators.py`
all exist to make sure the AI never presents an unconfirmed claim as
settled fact.

**Safety engine** — `backend/app/safety/red_flags.py` evaluates the
symptom tags gathered so far against `config/red_flags/rules.json` and
raises an `Alert`, never a diagnosis. Patient-facing copy is sanitized
through `safety/validators.py` before it is ever shown.

## Reusing this skeleton for another product

To turn this into, say, an insurance or education intake assistant:
replace `config/questions/`, `config/red_flags/`, prompts inside
`ai_service.py`, and the domain models in `backend/app/models/` — leave
the layering, the AIProvider abstraction, the API response envelope, and
the frontend component library as-is.
