# 🚀 Latam Airlines Code Challenge SWE

A modular, production-ready FastAPI application for managing users, following best practices in API design, logging, error handling, and testing.

---

## 📦 Features

- ✅ **FastAPI + SQLModel** (SQLite with upgrade path to PostgreSQL)
- ✅ Modular architecture (separation of models, services, schemas, and API)
- ✅ Custom exception handling with consistent API responses
- ✅ Built-in pagination, input validation, and role-based enums
- ✅ Full logging configuration with environment-controlled log levels
- ✅ Unit-tested with `pytest` and `monkeypatch` for isolated logic

---

## 📁 Project Structure

```
.
├── main.py                      # FastAPI app entry point
├── app/
│   ├── api/                     # Route definitions (v1)
│   ├── core/                    # Config, DB, logging setup
│   ├── models/                  # SQLModel database models
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── services/                # Business logic
│   ├── exceptions/             # Custom exception classes
├── tests/                      # Unit tests with mocked DB
│   ├── conftest.py
│   ├── test_users.py
└── .env                        # Environment configuration
```

---

## 📚 Endpoint Dictionary

| Method | Endpoint                  | Description                         | Body Required |
|--------|---------------------------|-------------------------------------|---------------|
| POST   | `/api/v1/users/`          | Create a new user                   | ✅            |
| GET    | `/api/v1/users/`          | Get paginated list of users         | ❌            |
| GET    | `/api/v1/users/{id}`      | Get user by ID                      | ❌            |
| PUT    | `/api/v1/users/{id}`      | Update user fields                  | ✅            |
| DELETE | `/api/v1/users/{id}`      | Delete user by ID                   | ❌            |

### 🔎 Query Parameters

- `GET /users`
  - `page` (int, default: 1)
  - `limit` (int, default: 10)

> All endpoints return a standardized `APIResponse` with status, message, and timestamp.

---

## 💡 API Response Format

All endpoints return a consistent response shape:

```json
{
  "status": "success",
  "data": {...},
  "message": "User created successfully.",
  "response_time": "2025-04-11T20:00:00Z"
}
```

For errors:

```json
{
  "status": "error",
  "data": null,
  "message": "User with ID 99 not found.",
  "response_time": "2025-04-11T20:05:00Z"
}
```

---

## 🧰 Logging Setup

- Configured via `app/core/logging_config.py`
- Log level set using `.env`:

```env
LOG_LEVEL=INFO
```

- Output format:

```bash
[2025-04-11 22:00:00] [INFO] app.services.user_service: User deleted
```

---

## 🧪 Testing

### ✅ Unit tests using `pytest` and `monkeypatch`

- Fully mocked DB session (`get_session()`)
- Service functions are patched to isolate API behavior

```bash
pytest
```

### ✅ Example test:

```python
def test_create_user_success(client, monkeypatch):
    monkeypatch.setattr("app.services.users.create_user", mock_create_user)
    ...
```

---

## 🚀 Getting Started

### 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Environment config

```env
DATABASE_URL=$DATABASE_URL
LOG_LEVEL=DEBUG
```

### ▶️ Run the app

```bash
uvicorn main:app --reload
```

### 🧪 Run tests

```bash
pytest
```

---

## 📌 TODO / Roadmap

- [ ] JWT authentication
- [ ] Swagger security schema
- [ ] Role-based access control
- [ ] Alembic integration for migrations
- [ ] Dockerfile for deployment

---

## 📄 License

MIT — feel free to use this architecture as a starter for your next API project.

---

## ✨ Author

Built with ❤️ by Luis Enrique Ramirez Roque
GitHub: [https://github.com/luisEnriqueR/latam_challenge](https://github.com/luisEnriqueR/latam_challenge)
