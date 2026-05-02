# Technical Debt

## Debt 1 — SQLite instead of PostgreSQL

- **Reason:** Faster implementation for demo.
- **Interest:** Limited concurrency and less production realism.
- **Paydown plan:** Replace SQLite with PostgreSQL in Docker Compose.

## Debt 2 — Simple frontend without framework

- **Reason:** Faster to implement and easier to explain.
- **Interest:** Harder to maintain if UI grows.
- **Paydown plan:** Migrate to React/Vite.

## Debt 3 — In-memory cache

- **Reason:** Satisfies caching requirement with minimal complexity.
- **Interest:** Cache is lost on restart and not shared between instances.
- **Paydown plan:** Use Redis.

## Debt 4 — Limited automated tests

- **Reason:** Time constraint.
- **Interest:** More risk when changing endpoints.
- **Paydown plan:** Add service-layer tests and integration tests.
