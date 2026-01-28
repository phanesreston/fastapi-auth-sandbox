# Auth Sandbox API

A learning-focused FastAPI project demonstrating:

- JWT-based authentication
- Bearer token authorization
- Role-based access control (user/admin)
- OpenAPI / Swagger integration

## Tech Stack
- Python
- FastAPI
- JWT (python-jose)

## Endpoints
- `POST /login`
- `GET /protected`
- `GET /admin`

## Run locally
```bash
uvicorn main:app --reload

