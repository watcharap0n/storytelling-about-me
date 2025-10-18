# Kane Portfolio API

Structured JSON API powering Watcharapon “Kane” Weeraborirak’s AI & cloud engineering portfolio. The API is optimised for MCP tools, chatbots, and automation flows (e.g., n8n) with strict JSON contracts, rate limiting, and API key authentication.

## Features
- FastAPI-based, production-focused codebase with seed data (`data/seed.json`).
- Secure by default: `x-api-key` header, 60 req/min per IP, correlation IDs, request logging.
- CORS policy: GET endpoints accessible publicly; cross-origin POST limited to contact/chat.
- Comprehensive resources: about, pillars, work, experience, skills, certifications, availability, contact, chat.
- Health checks, system metadata, `/v1` index for resource discovery.
- Generated OpenAPI 3.1 spec (`openapi.yaml`) and MCP tool manifest (`mcp.tools.json`).

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set API_KEY etc.
uvicorn app.main:app --reload
```

### Environment Variables
` .env.example ` documents the full set. Minimum required:

| Variable | Description |
|----------|-------------|
| `API_KEY` | Shared API key expected in `x-api-key` |
| `N8N_WEBHOOK_URL` | Optional contact message webhook |
| `CALENDAR_SOURCE_URL` | Optional ICS/Google calendar source (future use) |
| `RAG_ENDPOINT` | Optional external RAG endpoint (future use) |

### Docker (optional)
```
docker build -t kane-portfolio-api .
docker run -p 8000:8000 --env-file .env kane-portfolio-api
```

## Endpoints Overview
All versioned endpoints require `x-api-key`. GET endpoints accept cross-origin requests; POST is whitelisted for `/v1/contact/message` and `/v1/chat/ask` only.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/healthz` | GET | Health probe |
| `/v1` | GET | Resource index |
| `/v1/meta` | GET | Build & environment info |
| `/v1/about` | GET | Profile headline & links |
| `/v1/pillars` | GET | Capability pillars |
| `/v1/work` | GET | Case studies list (optional `limit`) |
| `/v1/work/{slug}` | GET | Case study detail |
| `/v1/experience` | GET | Career timeline |
| `/v1/skills` | GET | Skill groups (1–5 scale) |
| `/v1/certifications` | GET | Certifications & trainings |
| `/v1/contact` | GET | Contact channels |
| `/v1/contact/message` | POST | Create contact ticket and forward to n8n |
| `/v1/availability` | GET | Free/busy windows (optional `range` interval) |
| `/v1/availability/hold` | POST | Soft-hold 30-minute slot |
| `/v1/chat/ask` | POST | Lightweight Q&A over portfolio content |

Standard error model:
```json
{
  "error": {
    "code": "ERR_NOT_FOUND",
    "message": "Work item not found.",
    "correlation_id": "uuid"
  }
}
```

## MCP Tool Manifest
`mcp.tools.json` maps each REST resource to a tool definition for MCP clients.

## OpenAPI Spec
Generated snapshot lives at `openapi.yaml`. Regenerate after changes via:
```bash
python scripts/generate_openapi.py
```

## Testing
```
pytest
```

## cURL Examples
```bash
curl -H "x-api-key: $API_KEY" http://localhost:8000/v1/about

curl -X POST http://localhost:8000/v1/contact/message \
  -H "x-api-key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"Alex","email":"alex@example.com","message":"Let’s collaborate!"}'
```

---
Seed data may be replaced with live sources later; schemas stay stable for downstream agents.
