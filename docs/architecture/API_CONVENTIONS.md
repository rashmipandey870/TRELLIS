# TRELLIS API Conventions, Request/Response Protocols & Error Model

## 1. Architectural Baseline
TRELLIS APIs adhere to RESTful principles, versioned under `/api/v1/`, powered by FastAPI and fully documented via auto-generated OpenAPI 3.1 schemas.

### Core Standards
- **Serialization**: JSON UTF-8 encoding.
- **Timestamps**: All timestamps are formatted strictly as ISO 8601 in UTC (`YYYY-MM-DDTHH:MM:SS.mmmmmmZ`).
- **Naming Conventions**: Backend Pydantic models use `snake_case`; responses are automatically serialized to `camelCase` for Angular frontend consumption via Pydantic alias generators.
- **Tenant Context**: Injected automatically via user session JWT (`org_id`); tenant tampering is blocked at the gateway.

---

## 2. Standard Request Headers

| Header Name | Mandatory / Optional | Purpose | Example |
|---|---|---|---|
| `Authorization` | Mandatory (protected routes) | Bearer JWT access token | `Bearer eyJhbGciOi...` |
| `X-Correlation-ID` | Generated if absent | Distributed tracing identifier across frontend, FastAPI, Celery, and MySQL | `corr-9f8a-42c1-b0e2-87a123` |
| `Idempotency-Key` | Mandatory on critical POSTs | Prevents duplicate state mutations (assessments, idea submissions, XP grants) | `idem-7b3d81fa-2234` |
| `Accept-Language` | Optional | Localization preference (`en-IN`, `hi-IN`) | `en-IN` |

---

## 3. Standardized Error Model (RFC 9457 Problem Details)

All error responses from the FastAPI backend return `application/problem+json` formatted according to RFC 9457:

```json
{
  "type": "https://trellis.csmtech.example.com/errors/permission-denied",
  "title": "Permission Denied",
  "status": 403,
  "detail": "Viewing this Growth Ring summary requires active consent from the employee via the Consent Passport.",
  "instance": "/api/v1/growth-ring/users/emp-4829",
  "code": "CONSENT_REQUIRED",
  "correlation_id": "corr-9f8a-42c1-b0e2-87a123",
  "timestamp": "2026-11-13T12:00:00.000000Z",
  "errors": [
    {
      "field": "consent_status",
      "reason": "PURPOSE_MANAGER_SUMMARY_SHARE is not granted by user emp-4829"
    }
  ]
}
```

### Standard HTTP Status Codes

| HTTP Status | Semantics in TRELLIS | Typical Trigger |
|---|---|---|
| `200 OK` | Successful query or idempotent update. | Reading a Growth Ring, listing courses. |
| `201 Created` | Successful creation of a new entity. | Submitting an idea, recording an assessment attempt. |
| `204 No Content` | Successful deletion or state change with no body. | Revoking a consent grant. |
| `400 Bad Request` | Malformed JSON or business logic violation. | Submitting invalid answers, negative XP amounts. |
| `401 Unauthorized` | Missing, expired, or signature-invalid JWT. | Session expired, invalid token. |
| `403 Forbidden` | Denied by Policy Engine (`can()`). | Manager attempting to view unconsented personal data. |
| `404 Not Found` | Entity does not exist within the tenant scope. | Pathway ID not found in tenant. |
| `409 Conflict` | Optimistic concurrency conflict or duplicate key. | Stale hash in evidence ledger append. |
| `422 Unprocessable Entity` | Pydantic schema validation failure. | Missing required field, failed regex. |
| `429 Too Many Requests` | Redis token-bucket rate limit exceeded. | Rapid assessment submissions or AI coach queries. |
| `500 Internal Error` | Unexpected backend exception. | Correlation ID logged; PII stripped from client output. |

---

## 4. Cursor-Based Pagination Pattern

Collections with potentially large result sets use cursor-based pagination to guarantee predictable query performance and eliminate offset drift:

```json
{
  "items": [ ... ],
  "pagination": {
    "cursor": "ZXZpZGVuY2VfaWQ6MTA4",
    "has_more": true,
    "limit": 20,
    "total_count": 142
  }
}
```
