from database import task_queries


class FakeCursor:
    def __init__(self, returned_rows):
        self.returned_rows = iter(returned_rows)
        self.executed = []
        self.executed_many = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, query, parameters):
        self.executed.append((query, parameters))

    def executemany(self, query, parameters):
        self.executed_many.append((query, parameters))

    def fetchone(self):
        return next(self.returned_rows)


class FakeConnection:
    def __init__(self, cursor):
        self.fake_cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def cursor(self):
        return self.fake_cursor


def test_add_task_saves_description_and_links_existing_and_new_tags(monkeypatch):
    cursor = FakeCursor(returned_rows=[(41,), (8,)])
    monkeypatch.setattr(
        task_queries,
        "get_db_connection",
        lambda: FakeConnection(cursor),
    )
    task = {
        "task": "Schema project",
        "course_id": 3,
        "estimated_hours": 6,
        "hours_used": None,
        "status": "not_started",
        "difficulty": 4,
        "due_date": "2026-08-15",
        "date_completed": None,
        "short_description": "Create and document the relational schema.",
    }
    tags = [
        {"tag_id": 5, "tag_name": "Project", "color_hex": "#8B5CF6"},
        {"tag_name": "Database", "color_hex": "#3B82F6"},
    ]

    task_id = task_queries.add_task(7, task, tags)

    assert task_id == 41
    assert cursor.executed[0][1][-1] == task["short_description"]
    assert cursor.executed[1][1] == (7, "Database", "#3B82F6")
    assert cursor.executed_many[0][1] == [(7, 41, 5), (7, 41, 8)]


def test_add_task_deduplicates_selected_tag_links(monkeypatch):
    cursor = FakeCursor(returned_rows=[(42,)])
    monkeypatch.setattr(
        task_queries,
        "get_db_connection",
        lambda: FakeConnection(cursor),
    )
    task = {
        "task": "Read chapter",
        "course_id": 2,
        "status": "not_started",
        "difficulty": 2,
        "short_description": None,
    }
    repeated_tag = {"tag_id": 5, "tag_name": "Reading", "color_hex": "#10B981"}

    task_queries.add_task(7, task, [repeated_tag, repeated_tag])

    assert cursor.executed_many[0][1] == [(7, 42, 5)]
