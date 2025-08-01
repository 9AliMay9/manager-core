# Version: core  
# 🧩 Entity Manager API · Core Module

This project is the **core foundation module** of the Entity Manager API series, implementing a standard dual-entity structure: `Sbj / Obj`. As the starting point of the entire platform architecture, it focuses on:

- Clear and minimal CRUD design  
- Data consistency with automatic timestamp maintenance  
- Educational clarity, designed to evolve into future functional modules (Authorization, Security, CI/CD, etc.)

> 📦 This version uses **synchronous FastAPI + SQLAlchemy 2.0**, making it easier to understand ORM models and transaction mechanisms.

---

## 🛠 Tech Stack

- **FastAPI** – A modern web framework with support for type hints and auto-generated documentation  
- **SQLAlchemy 2.0 (sync)** – Declarative and type-safe ORM in its new 2.0 style  
- **PostgreSQL** – Relational database system used as backend storage  
- **Alembic** – Database migration tool for SQLAlchemy  
- **PDM** – A modern Python dependency and package manager (requires Python ≥ 3.11)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/manager-core.git
cd manager-core
```

### 2. Install Dependencies

Make sure you have **Python 3.11+** and **PDM** installed. Then run:

```bash
pdm install
```

> ℹ️ This project uses [PDM](https://pdm.fming.dev/) for modern Python dependency and virtual environment management.

### 3. Configure Environment

Create your own `.env` file in the root directory. Example:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/your_db
```

Also, make sure to update your local `alembic.ini` file if necessary. It is **excluded from version control** (`.gitignore`).

### 4. Apply Database Migrations

Run Alembic migrations to initialize your PostgreSQL database:

```bash
pdm run alembic upgrade head
```

### 5. Start the Application

```bash
pdm run uvicorn app.main:app --reload
```

You should see the API running at:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

Auto-generated docs are available at:

* Swagger UI: `/docs`

---

## 🗂️ Project Structure

```bash
.
├── LICENSE
├── README.md
├── alembic/               # Alembic migration scripts
│   ├── env.py             # Migration environment setup
│   └── versions/          # Migration history
├── alembic.ini            # Alembic configuration (ignored by Git)
├── app/                   # Main application package
│   ├── config.py          # Environment and settings loader
│   ├── database.py        # Database session and engine setup
│   ├── init_db.py         # Optional DB initializer
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # SQLAlchemy model definitions
│   ├── crud/              # Data access logic (Sbj / Obj)
│   ├── routes/            # API route declarations
│   └── schemas/           # Pydantic schemas for input/output
├── pdm.lock
├── pyproject.toml         # Project and dependency definitions
├── src/manager_core/      # Package stub (for future packaging)
├── tests/                 # Placeholder for test modules
└── .env                   # Local environment variables (not tracked)
```
