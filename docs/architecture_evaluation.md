# Architecture Evaluation

## Scenario 1 — Performance

- **Stimulus:** Many users request the product list repeatedly.
- **Environment:** Normal demo environment.
- **Artifact:** `GET /api/v1/products`.
- **Response:** Backend returns the product list quickly.
- **Measure:** Cached responses should use `X-Cache: HIT`.

### Current status

Pass for simple demo.

### Risk

In-memory cache works only inside one backend instance.

### Mitigation

Use Redis cache in future if the backend is scaled horizontally.

---

## Scenario 2 — Availability

- **Stimulus:** Database becomes unavailable.
- **Environment:** Docker/local runtime.
- **Artifact:** `/ready` endpoint.
- **Response:** API returns `503` instead of crashing.
- **Measure:** `/ready` returns HTTP 503 when DB cannot be reached.

### Current status

Implemented with database check.

### Risk

SQLite is simple for demo, but not ideal for production concurrency.

### Mitigation

Move to PostgreSQL for production-like deployment.

---

## Scenario 3 — Security

- **Stimulus:** Normal user tries to create product through admin endpoint.
- **Environment:** Authenticated as role `user`.
- **Artifact:** `POST /api/v1/products`.
- **Response:** API returns `403 Forbidden`.
- **Measure:** No product is created.

### Current status

Implemented with `require_role("admin")`.

### Risk

JWT secret must be protected.

### Mitigation

Use environment variables and secret management.
