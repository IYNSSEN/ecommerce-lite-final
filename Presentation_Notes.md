# Presentation Notes

## Slide/story outline

1. Title and team
2. Problem: small online shop
3. Requirements: users, admin, products, orders
4. Architecture: frontend + Flask API + SQLite DB
5. Key decision: modular monolith
6. Data model: User, Product, Order, OrderItem
7. Security: JWT, password hashing, user/admin roles
8. DevOps: Docker Compose, CI, health/ready
9. Observability: JSON logs, requestId, status, latency
10. Demo
11. Risks and technical debt
12. Next steps

## Demo script

### Happy path

1. Open frontend.
2. Login as `user@example.com`.
3. Load products.
4. Create order.
5. Show my orders.

### Admin path

1. Login as `admin@example.com`.
2. Create a product.
3. Show product list updated.

### Failure / readiness path

1. Call `/health`.
2. Call `/ready`.
3. Explain that `/ready` checks database availability.
4. Show logs in backend terminal.

## Likely defense questions and answers

### 1. Why did you choose modular monolith?

Because the project scope and team size are limited. Modular monolith gives clear boundaries without microservice operational complexity.

### 2. What are the tiers?

Presentation tier is the frontend. Application tier is Flask REST API. Data tier is SQLite database.

### 3. Where are the security boundaries?

Protected endpoints are in the backend. JWT authentication identifies the user. Role middleware checks admin-only actions.

### 4. What is the difference between 401 and 403?

401 means the user is not authenticated. 403 means the user is authenticated but does not have permission.

### 5. How does the system handle failures?

The `/ready` endpoint checks dependencies. If the database is unavailable, it returns 503.

### 6. What technical debt remains?

SQLite, simple frontend, in-memory cache, and limited tests.

### 7. How would you improve the project?

Move to PostgreSQL, add Redis cache, add more tests, and migrate frontend to React.

### 8. What does CI do?

CI installs dependencies, runs tests, and checks whether Docker Compose builds.

### 9. What is cached?

The product list endpoint is cached for 60 seconds.

### 10. How do you prevent normal users from admin actions?

Admin endpoints use role-based authorization and require the `admin` role.
