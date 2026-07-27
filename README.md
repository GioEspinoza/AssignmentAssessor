<div align="center">

# Assignment Assessor

### A desktop academic planner that turns deadlines into an actionable study plan.

[![CI](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml/badge.svg)](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1F6AA5)](https://github.com/TomSchimansky/CustomTkinter)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-30%20passing-22C55E)](#quality)

[Overview](#overview) · [Screenshots](#screenshots) · [Architecture](#architecture) · [Setup](#local-setup) · [Roadmap](#roadmap)

</div>

---

## Overview

Assignment Assessor helps students answer a deceptively difficult question:
**what should I work on next?**

The application combines assignment difficulty, remaining effort, and time
until the deadline into a priority score. A responsive desktop dashboard then
surfaces upcoming coursework, workload summaries, progress states, and study
recommendations.

Beyond the product itself, this repository demonstrates practical desktop
application engineering:

- A layered Python architecture with GUI-independent domain and service modules
- PostgreSQL persistence with user, course, and assignment relationships
- Salted PBKDF2-HMAC-SHA256 password storage
- Responsive, theme-aware CustomTkinter components
- Database-independent unit tests and automated GitHub Actions checks
- A documented migration path from an early CLI prototype to a desktop product

## Screenshots

| Responsive dashboard | Authentication |
| :---: | :---: |
| <img src="docs/screenshots/dashboard.png" alt="Assignment Assessor dashboard" width="100%"> | <img src="docs/screenshots/authentication.png" alt="Assignment Assessor authentication screen" width="100%"> |

## Product highlights

### Academic workflow

- User-scoped courses and assignments
- Three assignment states: **Not Started**, **In Progress**, and **Completed**
- Upcoming-deadline sorting and overdue detection
- Search and status filtering
- Remaining-workload and completion summaries
- Priority-based study recommendations
- Course archiving that preserves assignment history

### Interface system

- Light and dark appearance modes
- Responsive typography without compounding font sizes
- Reusable dashboard cards and Linux mouse-wheel behavior
- Shared color, spacing, radius, and typography tokens
- Empty, selected, hover, and quick-view states

### Engineering

- Authentication, course, and task service boundaries
- Parameterized PostgreSQL queries
- Composite course ownership constraints
- Reproducible schema snapshot
- Isolated domain rules and input validation
- Active code separated from the archived CLI prototype

## How prioritization works

Open assignments receive a score based on their difficulty, remaining hours,
and deadline:

```text
remaining hours = max(estimated hours - hours used, 0)

priority = (difficulty × remaining hours) / days remaining
```

Assignments due today or already overdue use one day as the denominator. This
keeps the score finite while ensuring urgent work stays visible.

The study planner uses:

```text
recommended hours per day = remaining hours / days remaining
```

## Architecture

```mermaid
flowchart LR
    UI["gui_logic<br/>Screens & navigation"]
    Widgets["gui_widgets<br/>Reusable UI behavior"]
    Services["backend/*_service.py<br/>Application workflows"]
    Rules["backend/task_rules.py<br/>Domain rules"]
    Validation["backend/validation.py<br/>Input & date validation"]
    Queries["database/*_queries.py<br/>Parameterized SQL"]
    DB[("PostgreSQL")]

    UI --> Widgets
    UI --> Services
    Services --> Rules
    Services --> Validation
    Services --> Queries
    Queries --> DB
```

The key boundary is intentional: backend modules never import CustomTkinter,
fonts, colors, or widgets. Screens collect input and render results; services
coordinate workflows; rules remain deterministic and easy to test.

```text
AssignmentAssessor/
├── backend/          # services, task rules, validation, auth, and session
├── database/         # connection handling, query modules, and schema snapshot
├── gui_logic/        # CustomTkinter screens and navigation
├── gui_style/        # design tokens and responsive typography
├── gui_widgets/      # reusable visual components and widget behavior
├── tests/            # fast, database-independent unit tests
├── legacy/           # archived CLI prototype and compatibility logic
├── docs/             # architecture notes and application screenshots
└── main.py           # desktop application entry point
```

For a deeper walkthrough, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Data model

```mermaid
erDiagram
    USERS ||--o{ COURSES : owns
    USERS ||--o{ TASKS : creates
    COURSES ||--o{ TASKS : contains

    USERS {
        int user_id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        date join_date
    }

    COURSES {
        int course_id PK
        int user_id FK
        varchar course_name
        varchar course_code
        boolean is_active
    }

    TASKS {
        int task_id PK
        int user_id FK
        int course_id FK
        varchar task_name
        varchar status
        numeric estimated_hours
        numeric hours_used
        int difficulty_level
        date due_date
        date date_completed
    }
```

The composite task-to-course relationship ensures a task cannot reference
another user's course. Courses are archived with `is_active` instead of being
deleted, preserving historical assignments.

## Technology

| Area | Choice | Why |
| --- | --- | --- |
| Language | Python 3.12+ | Clear domain modeling and rapid desktop development |
| Desktop UI | CustomTkinter | Native desktop delivery with modern themed widgets |
| Database | PostgreSQL | Relational integrity, constraints, and reliable querying |
| Driver | Psycopg 3 | Modern PostgreSQL adapter with context-managed transactions |
| Security | PBKDF2-HMAC-SHA256 | Salted, iterative password hashing |
| Testing | Pytest | Fast unit coverage for rules and services |
| Quality | Ruff + GitHub Actions | Repeatable lint, test, and compile checks |

## Local setup

### Prerequisites

- Python 3.12 or newer
- PostgreSQL 14 or newer
- `psql` available from your terminal

### 1. Clone and install

```bash
git clone https://github.com/GioEspinoza/AssignmentAssessor.git
cd AssignmentAssessor

python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows:

```powershell
venv\Scripts\activate
```

### 2. Create the database

```bash
createdb assignment_assessor
psql -d assignment_assessor -f database/schema_snapshot.sql
```

The checked-in snapshot mirrors the authoritative PostgreSQL schema managed
through DataGrip.

### 3. Configure the connection

```bash
cp .env.example .env
```

Update `.env`:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/assignment_assessor
```

### 4. Run

```bash
python main.py
```

## Quality

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the same checks used by CI:

```bash
python -m pytest
ruff check .
python -m compileall -q backend database gui_logic gui_style gui_widgets main.py
```

The active suite is database-independent, making it fast enough for local
feedback and every push.

## Current state

The current desktop build includes authentication, the responsive dashboard,
course-aware persistence, assignment browsing, status filtering, quick views,
and the service/domain foundation for assignment creation and editing.

Some dashboard controls and the newest assignment form are intentionally still
being wired. The repository favors visible, accurate progress over presenting
unfinished behavior as production-ready.

## Roadmap

- Complete the remastered assignment creation and editing workflows
- Add course management and archive/restore screens
- Wire dashboard-wide search, profile, and notification actions
- Add calendar-based date selection and reminder scheduling
- Add PostgreSQL integration tests alongside the fast unit suite
- Expand analytics with workload and completion visualizations
- Package the desktop application for one-command installation

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Legacy prototype](legacy/README.md)

## Author

Built and designed by [Gio Espinoza](https://github.com/GioEspinoza).

If this project interests you, explore the service layer, schema constraints,
and responsive UI system—or open an issue with feedback.
