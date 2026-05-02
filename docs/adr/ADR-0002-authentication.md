# ADR-0002: Authentication and Authorization

## Status

Accepted

## Context

The project requires at least two roles and protected endpoints.

## Decision

We chose JWT-based authentication and role-based authorization.

- Passwords are hashed.
- Login returns a JWT.
- Client sends `Authorization: Bearer <token>`.
- Admin endpoints require the `admin` role.

## Consequences

### Pros

- Easy to test with curl and frontend.
- Stateless backend authentication.
- Clear 401 vs 403 behavior.

### Cons

- Token storage must be handled carefully.
- JWT secret must not be committed to repository.

## Alternatives

- Cookie-based session.
- External OAuth provider.
