<div align="center">

# Assignment Assessor

### A responsive desktop workspace for organizing coursework, deadlines, and study effort.

[![CI](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml/badge.svg)](https://github.com/GioEspinoza/AssignmentAssessor/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1F6AA5)](https://github.com/TomSchimansky/CustomTkinter)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-32%20passing-22C55E)](#quality)

[Overview](#overview) · [Screenshots](#screenshots) · [Features](#features) · [Architecture](#architecture) · [Setup](#local-setup) · [Roadmap](#roadmap)

</div>

---

## Overview

Assignment Assessor is a Python desktop application for turning a collection of
courses and deadlines into a manageable academic workflow. Students can create
an account, maintain course-scoped assignments, track progress, estimate
remaining effort, label work with reusable tags, and review upcoming work from
a responsive dashboard.

The project also serves as a practical example of layered desktop application
engineering:

- Modern, theme-aware interfaces built with CustomTkinter
- Responsive typography shared across authentication and application screens
- PostgreSQL persistence with user-level ownership constraints
- Transactional assignment, description, and tag creation
- GUI-independent task rules, validation, and service modules
- Fast unit tests backed by fakes instead of a required test database
- An archived CLI prototype showing the application's evolution

## Screenshots

### Authentication

Responsive login and registration tabs keep authentication focused while
sharing the same typography system as the main application.

<p align="center">
  <img src="docs/screenshots/Authentication.png" alt="Assignment Assessor login screen" width="100%">
</p>

### Dashboard

The dashboard combines workload totals, quick-action cards, appearance
controls, and an upcoming-assignment panel.

<p align="center">
  <img src="docs/screenshots/Dashboard.png" alt="Assignment Assessor dashboard" width="100%">
</p>

### Assignment workspace

Assignments can be searched and filtered by status. The split layout provides
a task list, selection-driven quick view, workload summary, and dedicated empty
states.

<p align="center">
  <img src="docs/screenshots/Assignments.png" alt="Assignment management screen" width="100%">
</p>

### Add assignment

The responsive assignment form collects course, difficulty, due date,
description, tags, status, and effort. Its course panel summarizes active work
and upcoming deadlines for the selected course.

<p align="center">
  <img src="docs/screenshots/Add%20Assignments.png" alt="Add Assignment form and course workload panel" width="100%">
</p>

## Features

### Available now

- Account registration and login with session-aware navigation
- Salted PBKDF2-HMAC-SHA256 password hashing
- User-scoped courses, assignments, and reusable tags
- Three assignment states: **Not Started**, **In Progress**, and **Completed**
- Assignment creation with:
  - Active-course selection and inline course creation
  - A five-level, color-graded difficulty selector
  - Calendar-based due-date selection
  - Optional short descriptions
  - Existing or newly created tags
  - Estimated remaining hours or completed hours
- Atomic assignment saves: the task, description, new tags, and tag links
  succeed or roll back together
- Origin-aware navigation: cancelling Add Assignment returns to either the
  dashboard or Assignments, depending on where it was opened
- Assignment search, status filtering, selectable rows, and quick views
- Dashboard summaries for due-soon, in-progress, and completed work
- Up-next sorting with overdue and approaching-deadline states
- Course workload counts and upcoming-work previews
- Light and dark appearance modes
- Responsive text across authentication, dashboard, assignment, and form screens
- Linux/X11 mouse-wheel support for nested scrollable widgets
- Course archive and restore support at the persistence layer

### In progress

The dashboard includes visual entry points for several planned modules. The
Assignments card and empty-state Add Assignment action are connected; the
following areas remain roadmap items:

- Urgent-work workspace
- Calendar view
- Study planner
- Analytics
- Lock-in/focus sessions
- Dashboard-wide search, notifications, and profile actions
- Course settings action beside the Add Assignment course selector

## Prioritization model

Open assignments can be ranked using difficulty, remaining effort, and the
number of days until the deadline:

```text
remaining hours = max(estimated hours - hours used, 0)

priority = (difficulty × remaining hours) / days remaining
```

Assignments due today or already overdue use one day as the denominator. This
keeps the score finite while ensuring urgent work remains visible.

The study recommendation helper uses:

```text
recommended hours per day = remaining hours / days remaining
```

## Architecture

```mermaid
flowchart LR
    UI["gui_logic<br/>Screens and navigation"]
    Widgets["gui_widgets<br/>Reusable interface behavior"]
    Style["gui_style<br/>Tokens and responsive text"]
    Services["backend/*_service.py<br/>Application workflows"]
    Rules["backend/task_rules.py<br/>Domain rules"]
    Validation["backend/validation.py<br/>Input and date validation"]
    Queries["database/*_queries.py<br/>Parameterized SQL"]
    DB[("PostgreSQL")]

    UI --> Widgets
    UI --> Style
    UI --> Services
    Services --> Rules
    Services --> Validation
    Services --> Queries
    UI --> Queries
    Queries --> DB
```

The long-term boundary is straightforward: screens collect and present data,
services coordinate application behavior, deterministic rules stay independent
of the GUI, and query modules own SQL and row mapping. Some newer assignment
creation behavior currently calls its query boundary directly and is a
candidate for continued service-layer consolidation.

```text
AssignmentAssessor/
├── backend/          # authentication, sessions, services, rules, validation
├── database/         # PostgreSQL connection, queries, and schema snapshot
├── gui_logic/        # CustomTkinter screens, forms, and navigation
├── gui_style/        # colors, spacing, typography, responsive scaling
├── gui_widgets/      # dashboard cards, tag selector, shared widget behavior
├── tests/            # database-independent unit and query-boundary tests
├── legacy/           # archived command-line prototype
├── docs/             # architecture notes and current screenshots
└── main.py           # desktop application entry point
```

For a deeper walkthrough, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Data model

```mermaid
erDiagram
    USERS ||--o{ COURSES : owns
    USERS ||--o{ TASKS : creates
    USERS ||--o{ TAGS : defines
    COURSES ||--o{ TASKS : contains
    TASKS ||--o{ TASK_TAGS : receives
    TAGS ||--o{ TASK_TAGS : labels

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
        date date_created
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
        text short_description
    }

    TAGS {
        int tag_id PK
        int user_id FK
        varchar tag_name
        varchar color_hex
        timestamp date_created
    }

    TASK_TAGS {
        int user_id FK
        int task_id FK
        int tag_id FK
    }
```

Composite ownership constraints prevent assignments and tags from crossing user
boundaries. Courses use `is_active` for archiving, preserving historical
assignments while excluding archived courses from new-assignment choices. Tag
names are unique per user without regard to letter casing.

## Technology

| Area | Choice | Purpose |
| --- | --- | --- |
| Language | Python 3.12+ | Application and domain implementation |
| Desktop UI | CustomTkinter | Modern, theme-aware desktop widgets |
| Date input | tkcalendar | Calendar-based due-date selection |
| Color input | CTkColorPicker | Custom reusable tag colors |
| Images | Pillow | Theme-aware interface assets |
| Database | PostgreSQL 14+ | Relational persistence and integrity |
| Driver | Psycopg 3 | Parameterized SQL and context-managed transactions |
| Configuration | python-dotenv | Local database connection configuration |
| Security | PBKDF2-HMAC-SHA256 | Salted iterative password hashing |
| Testing | Pytest | Fast unit and query-boundary coverage |
| Quality | Ruff + GitHub Actions | Automated lint, test, and compile checks |

## Local setup

### Prerequisites

- Python 3.12 or newer
- PostgreSQL 14 or newer
- PostgreSQL command-line tools (`createdb` and `psql`)
- Tk support for your Python installation

On Debian or Ubuntu, Tk can be installed with:

```bash
sudo apt install python3-tk
```

### 1. Clone the repository

```bash
git clone https://github.com/GioEspinoza/AssignmentAssessor.git
cd AssignmentAssessor
```

### 2. Create and activate a virtual environment

Linux or macOS:

```bash
python -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Install the runtime dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

```bash
createdb assignment_assessor
psql -d assignment_assessor -f database/schema_snapshot.sql
```

The checked-in schema snapshot contains the tables, indexes, constraints, and
relationships needed by the current application.

### 4. Configure the connection

Linux or macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Set your local connection string in `.env`:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/assignment_assessor
```

Do not commit `.env`; it is intended for local credentials only.

### 5. Run the application

```bash
python main.py
```

## Quality

Install the development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the same checks used during development and CI:

```bash
python -m pytest
ruff check .
python -m compileall -q backend database gui_logic gui_style gui_widgets main.py
```

The active test suite currently contains **32 passing tests** and does not
require a live PostgreSQL instance.

## Roadmap

- Build the urgent-work view from the existing priority rules
- Add a monthly calendar for assignments and events
- Complete study-planning and focus-session workflows
- Add workload and completion analytics
- Implement course management behind the course settings control
- Wire dashboard search, notification, and profile actions
- Add due-time persistence, reminders, and scheduling
- Move remaining GUI-to-query workflows behind service boundaries
- Add PostgreSQL integration tests alongside the fast unit suite
- Package the application for one-command desktop installation

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Legacy prototype](legacy/README.md)

## Author

Built and designed by [Gio Espinoza](https://github.com/GioEspinoza).

Contributions and constructive feedback are welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes.
