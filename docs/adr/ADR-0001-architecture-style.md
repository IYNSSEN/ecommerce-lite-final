# ADR-0001: Architecture Style

## Status

Accepted

## Context

The project must be demonstrable and defendable within a short university deadline. It requires frontend, backend, database, roles, API and documentation.

## Decision

We chose a **modular monolith**.

## Consequences

### Pros

- Easier to build and run.
- Easier to debug.
- Clear internal modules are still possible.
- Lower operational complexity than microservices.

### Cons

- Independent scaling of modules is not possible.
- A larger future system may need service extraction.

## Alternatives

- Microservices with separate services.
- Simple monolith without clear modules.
