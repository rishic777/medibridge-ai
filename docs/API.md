# API Reference

Base URL: `http://localhost:8000/api/v1`

All responses use a consistent envelope:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": { "request_id": "..." }
}
```

Errors:

```json
{
  "success": false,
  "data": null,
  "error": { "code": "INVALID_PATIENT", "message": "Patient could not be found." },
  "meta": { "request_id": "..." }
}
```

## Patients

| Method | Path | Description |
|---|---|---|
| POST | `/patients` | Create a patient |
| GET | `/patients/{id}` | Get a patient |
| GET | `/patients` | List patients |
| GET | `/patients/{id}/alerts` | Alerts for one patient |

## Conversations

| Method | Path | Description |
|---|---|---|
| POST | `/conversations` | Start a conversation (`{ patient_id }`) |
| POST | `/conversations/{id}/message` | Send a message, get AI reply + next question |
| GET | `/conversations/{id}` | Get full conversation transcript |

## AI

| Method | Path | Description |
|---|---|---|
| POST | `/ai/extract` | Extract structured symptoms from free text |
| POST | `/ai/question` | Get the next adaptive question for a condition |
| POST | `/ai/summary` | Generate a plain-language patient summary |

## Documents

| Method | Path | Description |
|---|---|---|
| POST | `/reports/upload?patient_id=...` | Upload a report file (multipart) |
| POST | `/reports/{id}/process` | Run OCR + AI extraction on an uploaded report |
| GET | `/reports/{id}` | Get report + extracted data |

## Safety

| Method | Path | Description |
|---|---|---|
| POST | `/safety/check` | Evaluate a set of symptom tags against red-flag rules |
| GET | `/alerts` | All unacknowledged alerts (doctor dashboard feed) |
| PATCH | `/alerts/{id}/acknowledge` | Acknowledge an alert |

## Verification / History

| Method | Path | Description |
|---|---|---|
| GET | `/history/{patient_id}` | Structured patient history with verification sources |
| POST | `/history/{patient_id}/verify` | Move a fact along patient → document → physician-verified |

## Doctors

| Method | Path | Description |
|---|---|---|
| GET | `/doctors/dashboard` | Summary counts for the dashboard landing view |

Interactive docs are also available at `/docs` (Swagger UI) once the
backend is running.
