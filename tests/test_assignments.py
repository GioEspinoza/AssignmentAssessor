import pytest

from gui_logic.assignments import (
    build_quick_view_details,
    build_task_action_items,
    get_assignment_list_feedback,
)


def test_task_action_items_keep_required_order_and_callback_bindings():
    task = {"task_id": 17, "task": "Linked structures"}
    calls = []

    def record_action(action, selected_task):
        calls.append((action, selected_task))

    items = build_task_action_items(task, record_action)

    assert [item["action"] for item in items] == ["view", "edit", "delete"]
    assert [item["label"] for item in items] == [
        "View Task",
        "Edit Task",
        "Delete Task",
    ]
    assert [item["danger"] for item in items] == [False, False, True]

    for item in items:
        item["command"]()

    assert calls == [
        ("view", task),
        ("edit", task),
        ("delete", task),
    ]


@pytest.mark.parametrize(
    ("total_count", "visible_count", "expected_feedback"),
    [
        (0, 0, "empty"),
        (3, 0, "no_results"),
        (3, 1, "end"),
        (3, 3, "end"),
    ],
)
def test_assignment_list_feedback_distinguishes_empty_filtered_and_end_states(
    total_count,
    visible_count,
    expected_feedback,
):
    assert get_assignment_list_feedback(total_count, visible_count) == expected_feedback


@pytest.mark.parametrize(
    (
        "tags",
        "description",
        "expected_tags",
        "expected_description",
        "show_tags_placeholder",
        "show_description_placeholder",
    ),
    [
        (
            [
                {
                    "tag_id": 4,
                    "tag_name": "Homework",
                    "color_hex": "#3B82F6",
                },
                {
                    "tag_id": 9,
                    "tag_name": "Reading",
                    "color_hex": "#10B981",
                },
            ],
            "  Review chapters one through three.  ",
            (
                {
                    "tag_id": 4,
                    "tag_name": "Homework",
                    "color_hex": "#3B82F6",
                },
                {
                    "tag_id": 9,
                    "tag_name": "Reading",
                    "color_hex": "#10B981",
                },
            ),
            "Review chapters one through three.",
            False,
            False,
        ),
        (
            [
                {
                    "tag_id": 4,
                    "tag_name": "Homework",
                    "color_hex": "#3B82F6",
                },
            ],
            "   ",
            (
                {
                    "tag_id": 4,
                    "tag_name": "Homework",
                    "color_hex": "#3B82F6",
                },
            ),
            None,
            False,
            True,
        ),
        (
            None,
            "Read the linked research notes.",
            (),
            "Read the linked research notes.",
            True,
            False,
        ),
        (
            [],
            "\n\t ",
            (),
            None,
            True,
            True,
        ),
    ],
    ids=(
        "tags-and-description",
        "tags-only",
        "description-only",
        "neither",
    ),
)
def test_quick_view_details_cover_all_optional_content_combinations(
    tags,
    description,
    expected_tags,
    expected_description,
    show_tags_placeholder,
    show_description_placeholder,
):
    task = {
        "task_id": 17,
        "task": "Linked structures",
        "short_description": description,
    }

    details = build_quick_view_details(task, tags)

    assert details["tags"] == expected_tags
    assert details["description"] == expected_description
    assert details["tags_placeholder"] == ("No tags added." if show_tags_placeholder else None)
    assert details["description_placeholder"] == (
        "No description provided." if show_description_placeholder else None
    )
