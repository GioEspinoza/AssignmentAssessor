# Assignment Assessor

[![CI](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml/badge.svg)](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1f6aa5)](https://github.com/TomSchimansky/CustomTkinter)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Assignment Assessor is a desktop academic planner that helps students decide
what to work on next. It combines assignment difficulty, estimated effort, and
time remaining into a priority score, then turns that information into a daily
study recommendation.

The project demonstrates layered Python application design, secure credential
storage, PostgreSQL CRUD operations, automated tests, and a reusable
CustomTkinter design system.

> The dashboard now includes responsive navigation cards, summary panels,
> upcoming assignments, search and account-action placeholders, and a
> scrollable content area. Navigation wiring for the newest controls is still
> in progress.

## Highlights

- Multi-user registration and login with salted PBKDF2 password hashes
- User-scoped assignment storage backed by PostgreSQL
- Create, read, update, complete, and delete assignment workflows
- Priority ranking for incomplete and overdue work
- Daily study-hour recommendations
- Shared typography, color, and spacing tokens for consistent UI styling
- Unit-tested business and authentication logic
- GitHub Actions checks for tests, linting, and syntax

## Screenshots

Screenshots are coming soon. Add new images to `docs/screenshots/` and replace
the placeholders below as the interface develops.

| Dashboard | Authentication |
| --- | --- |
| _Dashboard screenshot coming soon_ | _Login screenshot coming soon_ |

## How prioritization works

For each incomplete assignment:

```text
priority = (difficulty × estimated hours) / days remaining
```

Assignments due today or already overdue use one day as the denominator. This
keeps the result finite while ensuring urgent work receives a high score.

Study-plan recommendations use:

```text
recommended hours per day = estimated hours / days remaining
```

## Architecture

```text
AssignmentAssessor/
├── assets/           # light and dark interface icons
├── backend/          # validation, authentication, session, and priority logic
├── database/         # PostgreSQL connection and query modules
├── docs/screenshots/ # application screenshots for project documentation
├── gui_logic/        # CustomTkinter screens and navigation
├── gui_style/        # typography, color, and spacing design tokens
├── gui_widgets/      # reusable UI component package
├── tests/            # database-independent business-logic tests
└── main.py           # desktop application entry point
```

The UI calls the business and database layers through focused modules instead
of embedding SQL or password logic directly in widgets.

## Local setup

### Prerequisites

- Python 3.12 or newer
- PostgreSQL 14 or newer

### Installation

```bash
git clone https://github.com/GioEspinoza/AssignmentAssessor.git
cd AssignmentAssessor
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
venv\Scripts\activate
```

### Database

The repository includes a generated snapshot of the authoritative
DataGrip-managed schema. Make schema changes in DataGrip, then regenerate this
snapshot from the live database; do not edit it manually.

Create a PostgreSQL database and apply the snapshot with:

```bash
psql -d assignment_assessor -f database/schema_snapshot.sql
```

Copy the environment template and replace the example connection string:

```bash
cp .env.example .env
```

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/assignment_assessor
```

The snapshot is documentation and a reproducible setup aid, not the primary
schema-editing workflow.

### Run the application

```bash
python main.py
```

## Development

Install development dependencies and run the quality checks:

```bash
pip install -r requirements-dev.txt
python -m pytest
ruff check .
python -m compileall -q backend database gui_logic gui_style gui_widgets main.py
```

Database integration requires a configured PostgreSQL instance. The unit test
suite is intentionally database-independent and runs without a `.env` file.

## Security

Passwords are stored as salted PBKDF2-HMAC-SHA256 hashes, never as plaintext.
Local environment files are excluded from version control. See
[SECURITY.md](SECURITY.md) for responsible disclosure guidance.

## Roadmap

- Wire dashboard search, notifications, profile, and quick-action navigation
- Replace free-text dates with a calendar date picker
- Add password recovery and account-management flows
- Add database integration tests
- Add reminders and workload visualizations

## Author

Built by [Gio Espinoza](https://github.com/GioEspinoza).
