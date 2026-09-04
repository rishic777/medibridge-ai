# MediBridge AI

**AI-assisted patient history. Human-verified clinical insight.**

A modular prototype for an AI-assisted patient intake platform: patients
tell their story by voice or text, an adaptive question engine fills in
the clinically relevant gaps, a safety engine flags anything urgent, and
a doctor dashboard lets a clinician verify everything before it becomes
part of the official record. Nothing the AI produces is ever presented
to a patient as a diagnosis.

> This is a working starter codebase built from a general architecture
> brief, not from a specific problem statement — the AI prompts,
> question set, and red-flag rules are reasonable defaults meant to be
> edited (see `/config`) to match your exact requirements once you have
> them.

## Why it's structured this way

Nothing here is hard-coded into one big app. The UI, AI logic, question
flows, safety rules, database models, and third-party integrations are
separate layers (see `docs/architecture.md`), so:

- swapping AI vendors means editing one file (`ai_providers.py`), not the app
- changing the interview questions or safety rules means editing JSON in `/config`, not Python
- the same skeleton can become a different AI-assisted intake product later by replacing only the content layers

## Project layout

```
medibridge-ai/
├── frontend/     React + Vite patient & doctor UI
├── backend/      FastAPI: API, AI/OCR/speech services, safety engine
├── database/     PostgreSQL schema + seed data
├── config/       Questions, red-flag rules, language strings (edit without a deploy)
├── docs/         architecture.md, API.md, setup.md
├── docker-compose.yml
└── .env.example
```

## Quick start

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

Frontend: http://localhost:5173 · Backend docs: http://localhost:8000/docs

See `docs/setup.md` for the manual (non-Docker) setup and for how to
switch AI providers.

## Patient flow

```
Landing → Language → Registration → Consent → Symptom input (voice/text)
   → AI extraction → Adaptive questions → Red-flag check → Document upload
   → OCR → Structured history → Patient review
```

## Doctor flow

```
Doctor dashboard → Patient overview → Red flags → History timeline
   (each item badged: patient reported / document supported / physician verified)
   → Edit AI summary → Verify
```

## Design system

Colors, spacing, radii, and shadows are tokens in
`frontend/src/styles/tokens.css` — restyle the whole app by editing that
one file. Palette: white / deep blue (`#0B3C5D`) / blue (`#1976D2`) /
orange accent (`#F59E0B`), with semantic success/warning/danger/info
colors and WCAG-conscious contrast. Alerts never rely on color alone —
every urgent flag pairs a 🚨 icon with an explicit "URGENT" label.

## Safety by design

The system flags symptoms for clinician review — it never diagnoses.
Compare:

> ✅ "Potential red flag detected — clinician assessment recommended."
> ❌ "You have disease X."

`backend/app/safety/validators.py` sanitizes any AI-generated text before
it reaches a patient, and `backend/app/safety/red_flags.py` evaluates
config-driven rules (`config/red_flags/rules.json`) rather than
hard-coded logic.

## Next steps

1. Re-run this generator (or hand-edit `/config`) once you have the real
   problem statement / requirements doc, so questions, red-flag rules,
   and AI prompts match it exactly.
2. Wire a real AI provider: set `AI_PROVIDER=gemini` or `openai` and
   `AI_API_KEY` in `backend/.env`.
3. Add authentication for the doctor dashboard (a `doctors` table and
   `core/security.py` helpers are already scaffolded).
4. Review `docs/architecture.md` before extending any layer.
