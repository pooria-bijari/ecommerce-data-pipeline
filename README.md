# 🏗️ E-Commerce Data Pipeline (Production Edition)

A **production-style** data pipeline demonstrating modern data engineering practices:
Dockerized PostgreSQL, modular ETL with **type hints**, structured **logging**,
**unit tests** with pytest, SQL **views** for reporting, and **data quality checks**.

Unlike a tutorial project, this one is built the way real teams build pipelines:
config via environment variables, tests, logging, and containerization.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![pytest](https://img.shields.io/badge/pytest-passing-brightgreen?logo=pytest)

---

## 📖 Overview

This project ingests e-commerce transaction data, transforms it, loads it into
PostgreSQL, and exposes analytics through **SQL views**. It includes:

- 🐳 **Docker Compose** — spins up PostgreSQL in one command
- 📦 **Modular ETL** — `extract.py`, `transform.py`, `load.py`
- 🧪 **Unit tests** — `pytest` suite for transform and database layers
- 📊 **Analytics layer** — SQL views for common reporting needs
- ✅ **Data quality checks** — automated validation queries
- 📝 **Structured logging** — every run produces `logs/pipeline.log`

---

## 🏗️ Architecture

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Raw data    │───►│  src/extract.py │───►│  data/raw/       │
│  (generate)  │    │                 │    │  (parquet/csv)   │
└──────────────┘    └─────────────────┘    └────────┬─────────┘
                                                    │
                                                    ▼
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Postgres    │◄───│  src/transform  │───►│ data/transformed/│
│  + views     │    │  .py            │    │                  │
└──────┬───────┘    └─────────────────┘    └──────────────────┘
       │
       ▼
┌──────────────┐    ┌─────────────────┐
│  sql/*.sql   │───►│  Analytics &    │
│              │    │  data quality   │
└──────────────┘    └─────────────────┘
```

---

## 📁 Project Structure

```
ecommerce-data-pipeline/
├── src/
│   ├── __init__.py
│   ├── database.py           # SQLAlchemy engine + session
│   ├── extract.py            # Stage 1: extract
│   ├── transform.py          # Stage 2: transform
│   ├── load.py               # Stage 3: load to Postgres
│   ├── logger.py             # Structured logging setup
│   ├── run_analytics.py      # Runs analytics queries
│   ├── run_data_quality.py   # Runs quality checks
│   ├── create_views.py       # Creates SQL reporting views
│   ├── check_schema.py       # Verifies DB schema
│   └── generate_data.py      # Synthetic data generator
├── tests/
│   ├── test_database.py
│   └── test_transform.py
├── sql/
│   ├── create_tables.sql
│   ├── analytics.sql
│   ├── data_quality.sql
│   └── reporting_views.sql
├── data/
│   ├── raw/                  # (gitignored)
│   └── transformed/          # (gitignored)
├── logs/                     # (gitignored)
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop (for PostgreSQL)

### 1. Clone and enter

```bash
git clone https://github.com/pooria-bijari/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Set up environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
copy .env.example .env        # Windows
cp .env.example .env          # Mac/Linux
```

Edit `.env` with your PostgreSQL credentials (defaults match `docker-compose.yml`).

### 4. Start PostgreSQL

```bash
docker-compose up -d
```

### 5. Create schema and views

```bash
python src/check_schema.py
python src/create_views.py
```

### 6. Generate and process data

```bash
python src/generate_data.py
python src/extract.py
python src/transform.py
python src/load.py
```

### 7. Run analytics and quality checks

```bash
python src/run_analytics.py
python src/run_data_quality.py
```

---

## 🧪 Run Tests

```bash
pytest
```

Tests cover:
- Database connection and schema integrity
- Transform logic (cleaning, validation, feature creation)

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.10+ |
| Database | PostgreSQL 15 (via Docker) |
| ORM | SQLAlchemy |
| Testing | pytest |
| Config | python-dotenv |
| Logging | Python `logging` → file + console |
| Container | Docker + docker-compose |

---

## 🔮 Future Improvements

- [ ] Add **Apache Airflow** for scheduling
- [ ] Add **GitHub Actions** CI to run tests on every push
- [ ] Add **Great Expectations** for data validation
- [ ] Add **dbt** for the transform layer
- [ ] Add a **Streamlit dashboard** on top of the reporting views
- [ ] Add **Prometheus metrics** for pipeline monitoring

---

## 📝 What I Learned

- Structuring a Python project as a package (`src/`) with proper `__init__.py`
- Using `python-dotenv` to manage secrets — never hardcoding credentials
- Building a proper logging system instead of `print()`
- Writing tests with `pytest` for ETL logic
- Modeling a database schema in raw SQL and building reporting **views**
- Running PostgreSQL locally with Docker Compose

---

## 📄 License

MIT