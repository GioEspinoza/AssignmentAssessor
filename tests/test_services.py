from datetime import date, timedelta

from backend import (
    auth_service,
    course_service,
    session,
    tag_services,
    task_service,
)


def test_register_user_sets_session(monkeypatch):
    created_user = {
        "user_id": 7,
        "username": "Gio",
        "email": "gio@example.com",
    }

    monkeypatch.setattr(
        auth_service.user_queries,
        "get_user_by_username",
        lambda username: None,
    )
    monkeypatch.setattr(
        auth_service.auth,
        "hash_password",
        lambda password: b"hashed-password",
    )
    monkeypatch.setattr(
        auth_service.user_queries,
        "create_user",
        lambda username, email, password_hash: created_user,
    )
    monkeypatch.setattr(session, "current_user", None)

    user, error = auth_service.register_user(
        "Gio",
        "gio@example.com",
        "password123",
    )

    assert error is None
    assert user == created_user
    assert session.current_user == created_user


def test_authenticate_user_rejects_incorrect_password(monkeypatch):
    monkeypatch.setattr(
        auth_service.user_queries,
        "get_user_by_username",
        lambda username: {
            "user_id": 7,
            "username": username,
            "password_hash": b"stored-password",
        },
    )
    monkeypatch.setattr(
        auth_service.auth,
        "check_password",
        lambda password_hash, password: False,
    )

    user, error = auth_service.authenticate_user("Gio", "wrong-password")

    assert user is None
    assert error == "Incorrect password"


def test_task_service_filters_searches_and_summarizes():
    tasks = [
        {
            "task": "Read chapter",
            "course": "History",
            "status": "not_started",
            "estimated_hours": 4,
            "hours_used": None,
            "due_date": date.today(),
        },
        {
            "task": "Build schema",
            "course": "Databases",
            "status": "in_progress",
            "estimated_hours": 8,
            "hours_used": 3,
            "due_date": date.today() + timedelta(days=2),
        },
        {
            "task": "Submit essay",
            "course": "Writing",
            "status": "completed",
            "estimated_hours": 5,
            "hours_used": 5,
            "date_completed": date.today(),
            "due_date": None,
        },
    ]

    in_progress = task_service.filter_tasks_by_status(
        tasks,
        "in_progress",
    )
    search_results = task_service.search_tasks(tasks, "data")
    summary = task_service.get_task_summary(tasks)

    assert [task["task"] for task in in_progress] == ["Build schema"]
    assert [task["task"] for task in search_results] == ["Build schema"]
    assert summary["estimated_workload"] == 9
    assert summary["in_progress_tasks"] == 1
    assert summary["completed_tasks"] == 1


def test_dashboard_data_queries_tasks_once(monkeypatch):
    tasks = [
        {
            "task": "First",
            "course": "Testing",
            "status": "not_started",
            "estimated_hours": 2,
            "hours_used": None,
            "due_date": date.today() + timedelta(days=1),
        }
    ]
    calls = []

    def fake_get_tasks(user_id):
        calls.append(user_id)
        return tasks

    monkeypatch.setattr(task_service, "get_tasks", fake_get_tasks)

    dashboard_data = task_service.get_dashboard_data(12)

    assert calls == [12]
    assert dashboard_data["upcoming_tasks"] == tasks
    assert dashboard_data["summary"]["due_soon"] == 1


def test_due_state_distinguishes_today_from_this_week():
    assert task_service.get_due_state(date.today()) == "due_today"
    assert (
        task_service.get_due_state(date.today() + timedelta(days=1))
        == "due_soon"
    )


def test_get_due_status_text():
    assert task_service.get_due_status_text(date.today()) == "Due today"
    assert (
        task_service.get_due_status_text(date.today() + timedelta(days=1))
        == "Due in 1 day"
    )
    assert (
        task_service.get_due_status_text(date.today() + timedelta(days=4))
        == "Due in 4 days"
    )
    assert (
        task_service.get_due_status_text(date.today() - timedelta(days=1))
        == "Overdue"
    )


def test_available_tags_include_presets_and_custom_tags(monkeypatch):
    custom_tag = {
        "tag_id": 91,
        "tag_name": "Lab",
        "color_hex": "#123456",
    }
    monkeypatch.setattr(
        tag_services,
        "get_user_tags",
        lambda user_id: [custom_tag],
    )

    available_tags = tag_services.get_available_tags(7)
    available_names = {
        tag["tag_name"].strip().casefold()
        for tag in available_tags
    }

    assert {
        tag_name.casefold()
        for tag_name, _color_hex in tag_services.DEFAULT_TAGS
    } <= available_names
    assert "lab" in available_names


def test_available_tags_deduplicate_normalized_names(monkeypatch):
    persisted_homework = {
        "tag_id": 92,
        "tag_name": "  homework  ",
        "color_hex": "#654321",
    }
    monkeypatch.setattr(
        tag_services,
        "get_user_tags",
        lambda user_id: [persisted_homework],
    )

    available_tags = tag_services.get_available_tags(7)
    homework_tags = [
        tag
        for tag in available_tags
        if tag["tag_name"].strip().casefold() == "homework"
    ]

    assert len(homework_tags) == 1
    assert homework_tags[0]["tag_name"] == "homework"
    assert homework_tags[0]["tag_id"] == 92
    assert homework_tags[0]["color_hex"] == "#654321"


def test_course_service_reports_active_courses(monkeypatch):
    monkeypatch.setattr(
        course_service.course_queries,
        "get_active_courses",
        lambda user_id: [{"course_id": 3, "course_name": "Databases"}],
    )

    assert course_service.user_has_active_courses(7)
