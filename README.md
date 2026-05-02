# E-Commerce Lite — Multi-Tier Internet Application

This project is a small multi-tier e-commerce application prepared for the **Design of Multi-Tier Internet Applications** course.

## 1. System purpose

The application allows users to browse products and create orders. Admin users can create, update and delete products, and view all orders.

## 2. Architecture

The system has three tiers:

- **Presentation tier:** HTML/CSS/JavaScript frontend
- **Application tier:** Flask REST API
- **Data tier:** SQLite database

The backend uses a modular monolith style with controllers, services and repositories.

## 3. Main features

- User registration and login
- JWT-based authentication
- Role-based authorization: `user` and `admin`
- Product CRUD for admin
- Product listing for users
- Order creation for authenticated users
- Health and readiness endpoints
- Structured JSON request logs
- Basic caching for `GET /api/v1/products`
- Docker Compose local environment
- GitHub Actions CI

## 4. Demo accounts

After running the seed script:

| Role | Email | Password |
|---|---|---|
| admin | admin@example.com | admin123 |
| user | user@example.com | user123 |

## 5. Run locally without Docker

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python scripts/seed.py
python run.py
```

Then open frontend:

```bash
cd frontend
python -m http.server 5173
```

Open:

```text
http://localhost:5173
```

## 6. Run with Docker Compose

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:5000
```

Seed data inside Docker:

```bash
docker compose exec backend python scripts/seed.py
```

## 7. Health and readiness

```bash
curl http://localhost:5000/health
curl http://localhost:5000/ready
```

- `/health` checks if the API process is alive.
- `/ready` checks if the database dependency is reachable.

## 8. API endpoints

### Auth

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login and get JWT |
| GET | `/api/v1/auth/me` | Current user profile |

### Products

| Method | Endpoint | Role | Description |
|---|---|---|---|
| GET | `/api/v1/products` | public | List products |
| GET | `/api/v1/products/:id` | public | Get product |
| POST | `/api/v1/products` | admin | Create product |
| PUT | `/api/v1/products/:id` | admin | Update product |
| DELETE | `/api/v1/products/:id` | admin | Delete product |

### Orders

| Method | Endpoint | Role | Description |
|---|---|---|---|
| POST | `/api/v1/orders` | user/admin | Create order |
| GET | `/api/v1/orders/my` | user/admin | Show my orders |
| GET | `/api/v1/admin/orders` | admin | Show all orders |

## 9. Example curl flow

Login as user:

```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"user123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

List products:

```bash
curl http://localhost:5000/api/v1/products
```

Create order:

```bash
curl -X POST http://localhost:5000/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"items":[{"productId":1,"quantity":1}]}'
```

Login as admin:

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' | python -c "import sys,json; print(json.load(sys.stdin)['token'])")
```

Create product:

```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"name":"Demo Product","price":99.99,"stock":10,"description":"Created by admin"}'
```

## 10. Error model

Example validation error:

```json
{
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {"field": "name", "message": "Product name is required"}
    ]
  }
}
```

Common status codes:

- `200` success
- `201` created
- `204` deleted
- `400` validation error
- `401` unauthenticated
- `403` forbidden
- `404` not found
- `409` conflict
- `429` rate limited
- `503` not ready / dependency unavailable

## 11. Caching and performance

`GET /api/v1/products` uses an in-memory cache with a TTL of 60 seconds.

- Repeated product list requests can be served from cache.
- Product create/update/delete invalidates the product cache.
- The response header `X-Cache` shows `HIT` or `MISS`.

Example:

```bash
curl -i http://localhost:5000/api/v1/products
```

## 12. Security notes

- Passwords are hashed with Werkzeug password hashing.
- JWT is used for authentication.
- Admin endpoints require the `admin` role.
- Unauthorized requests return `401`.
- Forbidden role violations return `403`.
- Security headers are added.
- Login endpoint has basic rate limiting.
- Passwords and tokens are not logged.

## 13. CI

GitHub Actions runs:

- Python dependency installation
- pytest tests
- Docker Compose build

Workflow file:

```text
.github/workflows/ci.yml
```

## 14. Demo plan

1. Start the application.
2. Login as normal user.
3. List products.
4. Create an order.
5. Login as admin.
6. Create a product.
7. Show role-based access: normal user cannot create products.
8. Show `/health` and `/ready`.
9. Show logs in terminal.
10. Explain one limitation and one next step.
