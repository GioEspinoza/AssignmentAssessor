# Contributing

Thanks for taking an interest in Assignment Assessor.

## Development setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

Copy `.env.example` to `.env` and configure a local PostgreSQL connection when
working on database-backed screens.

## Before submitting a change

Run:

```bash
python -m pytest
ruff check .
python -m compileall -q backend database gui_logic gui_style gui_widgets main.py
```

## Project boundaries

- Put business rules and application workflows in `backend/`.
- Put SQL and row mapping in `database/`.
- Keep widget construction and navigation in `gui_logic/`.
- Add reusable CustomTkinter components to `gui_widgets/`.
- Do not import GUI packages, colors, or fonts from backend modules.
- Do not edit `database/schema_snapshot.sql` as the primary schema workflow;
  update the DataGrip-managed PostgreSQL schema and regenerate the snapshot.
- Keep new work out of `legacy/`.

## Style

- Follow the existing function-oriented code style.
- Prefer focused helpers over large screen callbacks.
- Use parameterized SQL for every query.
- Add or update tests for backend behavior.
- Keep user-facing documentation accurate about unfinished functionality.
- Keep README feature lists, technology choices, and roadmap items synchronized
  when a user-facing capability changes.
- Verify scrollable screens on Linux/X11 when changing shared mouse-wheel
  bindings; some composite CustomTkinter widgets reject direct `.bind()` calls.
