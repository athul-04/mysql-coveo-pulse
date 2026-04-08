# mysql-to-coveo-pulse

> FastAPI-powered pipeline to push Aiven MySQL data into Coveo — automated twice daily via GitHub Actions.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview

`mysql-to-coveo-pulse` is an automated data pipeline that fetches records from an **Aiven-hosted MySQL** database and pushes them into a **Coveo organization** using the Coveo Push API. The pipeline is exposed via a **FastAPI** application and runs on a scheduled cron job twice daily using **GitHub Actions**.

This project is designed to keep your Coveo index in sync with the latest data in your MySQL database — reliably, on a pulse.

---

## Architecture

```
Aiven MySQL DB
      │
      ▼
  FastAPI App  ──────►  Coveo Push API  ──────►  Coveo Index
      ▲
      │
GitHub Actions (Cron: 2x Daily)
```

**Flow:**
1. GitHub Actions triggers the pipeline on a cron schedule (twice daily).
2. The FastAPI app connects to the Aiven MySQL database and fetches the required records.
3. The fetched data is transformed into the Coveo document format.
4. The transformed documents are pushed to the Coveo source via the Coveo Push API.
5. Coveo indexes the documents and makes them searchable.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework to expose pipeline endpoints |
| **Aiven MySQL** | Cloud-hosted MySQL database (data source) |
| **Coveo Push API** | API to push documents into Coveo index |
| **GitHub Actions** | Workflow automation and cron scheduling |
| **SQLAlchemy** | ORM for MySQL database interaction |
| **Pydantic** | Data validation and schema definition |
| **httpx** | Async HTTP client for Coveo API calls |
| **python-dotenv** | Environment variable management |

---

## Prerequisites

Before setting up this project, make sure you have the following:

- **Python 3.10+** installed
- Access to an **Aiven MySQL** instance with valid credentials
- A **Coveo Organization** with a configured Push source
- A valid **Coveo API Key** with push permissions
- A **GitHub repository** with Actions enabled
- `pip` or `poetry` for dependency management

---

## Environment Variables

Create a `.env` file in the root of the project with the following variables:

```env
# Aiven MySQL
DB_HOST=your-aiven-mysql-host
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Coveo Push API
COVEO_ORG_ID=your_coveo_org_id
COVEO_SOURCE_ID=your_coveo_source_id
COVEO_API_KEY=your_coveo_api_key
COVEO_PUSH_URL=https://api.cloud.coveo.com/push/v1

# App Config
APP_ENV=production
LOG_LEVEL=INFO
```

> **Never commit your `.env` file.** Use GitHub Secrets for CI/CD.

### GitHub Secrets

Add the following secrets to your GitHub repository under `Settings → Secrets and Variables → Actions`:

| Secret Name | Description |
|---|---|
| `DB_HOST` | Aiven MySQL host |
| `DB_PORT` | Aiven MySQL port |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `COVEO_ORG_ID` | Coveo organization ID |
| `COVEO_SOURCE_ID` | Coveo push source ID |
| `COVEO_API_KEY` | Coveo API key with push permissions |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/mysql-to-coveo-pulse.git
cd mysql-to-coveo-pulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

### 5. Run the FastAPI app locally

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Trigger the pipeline manually

```bash
curl -X POST http://localhost:8000/api/v1/sync
```

You can also visit `http://localhost:8000/docs` to explore the interactive Swagger UI.

---

## GitHub Actions — Cron Setup

The pipeline is automated using a GitHub Actions workflow defined in `.github/workflows/sync.yml`.

### Schedule

The pipeline runs **twice daily** at:
- `00:00 UTC` (midnight)
- `12:00 UTC` (noon)

### Workflow file: `.github/workflows/sync.yml`

```yaml
name: Coveo Pulse Sync

on:
  schedule:
    - cron: '0 0 * * *'   # midnight UTC
    - cron: '0 12 * * *'  # noon UTC
  workflow_dispatch:        # allows manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run sync pipeline
        env:
          DB_HOST: ${{ secrets.DB_HOST }}
          DB_PORT: ${{ secrets.DB_PORT }}
          DB_NAME: ${{ secrets.DB_NAME }}
          DB_USER: ${{ secrets.DB_USER }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
          COVEO_ORG_ID: ${{ secrets.COVEO_ORG_ID }}
          COVEO_SOURCE_ID: ${{ secrets.COVEO_SOURCE_ID }}
          COVEO_API_KEY: ${{ secrets.COVEO_API_KEY }}
        run: python -m app.pipeline.sync
```

> You can also manually trigger the workflow from the **Actions** tab in your GitHub repository.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/api/v1/status` | Returns pipeline status and last sync time |
| `POST` | `/api/v1/sync` | Manually triggers the full sync pipeline |
| `GET` | `/docs` | Swagger UI (auto-generated) |

### Example — Trigger sync

**Request:**
```bash
POST /api/v1/sync
```

**Response:**
```json
{
  "status": "success",
  "records_fetched": 320,
  "records_pushed": 320,
  "timestamp": "2026-04-08T12:00:00Z"
}
```

---

## Project Structure

```
mysql-to-coveo-pulse/
├── app/
│   ├── main.py               # FastAPI app entry point
│   ├── config.py             # Environment config loader
│   ├── database/
│   │   ├── connection.py     # Aiven MySQL connection setup
│   │   └── queries.py        # SQL queries to fetch data
│   ├── coveo/
│   │   ├── client.py         # Coveo Push API client
│   │   └── mapper.py         # Maps DB records to Coveo document format
│   ├── pipeline/
│   │   └── sync.py           # Core sync orchestration logic
│   └── api/
│       └── routes.py         # FastAPI route definitions
├── .github/
│   └── workflows/
│       └── sync.yml          # GitHub Actions cron workflow
├── tests/
│   ├── test_sync.py
│   ├── test_coveo_client.py
│   └── test_db_queries.py
├── .env.example              # Sample environment variables
├── requirements.txt          # Python dependencies
├── README.md
└── LICENSE
```

---

## Contributing

Contributions are welcome! Please follow the guidelines below:

1. **Fork** the repository and create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Commit** your changes with a clear message:
   ```bash
   git commit -m "feat: add support for incremental sync"
   ```

3. **Push** and open a **Pull Request** against the `main` branch.

4. Ensure all tests pass before submitting:
   ```bash
   pytest tests/
   ```

### Branch Naming Convention

| Type | Pattern | Example |
|---|---|---|
| Feature | `feature/name` | `feature/incremental-sync` |
| Bug fix | `fix/name` | `fix/coveo-auth-error` |
| Chore | `chore/name` | `chore/update-dependencies` |

---


> Built with FastAPI · Powered by Aiven · Indexed by Coveo · Automated by GitHub Actions
