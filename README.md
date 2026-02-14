Notes is a professional note management system developed with modern web technologies, focusing on security and performance.

## Features

* Secure Identity Verification: User-based session management with JWT (JSON Web Token) and OAuth2.
* Advanced Note Management: Category, multi-tagging, and full-text search support.
* Pagination: Efficient listing in large datasets.
* Rate Limiting: Redis-based API request limiting (DoS and Brute Force protection).
* Dockerized Architecture: Set up the entire infrastructure with a single command.
* Database Migration: Sustainable database schema management with Alembic.

## Technology Stack

* Backend: FastAPI (Python 3.11+)
* Database: PostgreSQL
* Caching & Limiting: Redis
* ORM: SQLAlchemy
* Deployment: Docker & Docker Compose

## Install

1. Configure environmental variables:

Copy the `.env.example` file as `.env` and fill in the required fields:
```bash
cp .env.example .env
```

2. Start the system with Docker:
```bash
docker-compose up --build -d
```

3. Implement database migrations:
```bash
docker-compose exec web alembic upgrade head
```

The system is now ready!

-- API: `http://localhost:8000`

-- Swagger Documentation: `http://localhost:8000/docs`