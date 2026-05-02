# ADR-0003: Database Choice

## Status

Accepted

## Context

The project needs persistent data for users, products and orders.

## Decision

We use SQLite for the demo version because it is fast to set up and easy to run locally.

## Consequences

### Pros

- No separate database installation required.
- Very easy for local demo and defense.

### Cons

- Not ideal for production concurrency.
- Less realistic than PostgreSQL.

## Alternatives

- PostgreSQL with Docker Compose.
- MySQL or MariaDB.
