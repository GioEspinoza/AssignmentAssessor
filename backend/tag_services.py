import re

import psycopg

from database import tags_queries, task_queries


DEFAULT_TAGS = (
    ("Homework", "#3B82F6"),
    ("Exam", "#EF4444"),
    ("Project", "#8B5CF6"),
    ("Reading", "#10B981"),
    ("Low Priority", "#22C55E"),
    ("Medium Priority", "#F59E0B"),
    ("High Priority", "#DC2626"),
)

HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def _validate_user_id(user_id):
    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
        raise ValueError("A valid user_id is required.")


def _validate_tag_id(tag_id):
    if not isinstance(tag_id, int) or isinstance(tag_id, bool) or tag_id <= 0:
        raise ValueError("A valid tag_id is required.")


def _clean_tag_name(tag_name):
    clean_name = str(tag_name).strip()

    if not clean_name:
        raise ValueError("Tag name cannot be blank.")
    if len(clean_name) > 50:
        raise ValueError("Tag name cannot exceed 50 characters.")

    return clean_name


def _clean_color_hex(color_hex):
    clean_color = str(color_hex).strip().upper()

    if not HEX_COLOR_PATTERN.fullmatch(clean_color):
        raise ValueError("Tag color must use the format #RRGGBB.")

    return clean_color


def _clean_tag_ids(tag_ids):
    if tag_ids is None:
        return []

    clean_ids = []
    seen_ids = set()

    for tag_id in tag_ids:
        _validate_tag_id(tag_id)
        if tag_id not in seen_ids:
            clean_ids.append(tag_id)
            seen_ids.add(tag_id)

    return clean_ids


def _raise_friendly_constraint_error(error):
    constraint_name = error.diag.constraint_name

    if constraint_name == "tags_user_name_case_insensitive_unique":
        raise ValueError("A tag with that name already exists.") from error
    if constraint_name == "tags_color_hex_check":
        raise ValueError("Tag color must use the format #RRGGBB.") from error
    if constraint_name == "tags_name_not_blank_check":
        raise ValueError("Tag name cannot be blank.") from error

    raise error


def create_user_tag(user_id, tag_name, color_hex="#3B82F6"):
    _validate_user_id(user_id)
    clean_name = _clean_tag_name(tag_name)
    clean_color = _clean_color_hex(color_hex)

    try:
        return tags_queries.add_tag(user_id, clean_name, clean_color)
    except (psycopg.errors.UniqueViolation, psycopg.errors.CheckViolation) as error:
        _raise_friendly_constraint_error(error)


def get_user_tags(user_id):
    _validate_user_id(user_id)
    return tags_queries.get_tags(user_id)


def get_available_tags(user_id):
    return get_user_tags(user_id)


def update_user_tag(user_id, tag_id, tag_name, color_hex):
    _validate_user_id(user_id)
    _validate_tag_id(tag_id)
    clean_name = _clean_tag_name(tag_name)
    clean_color = _clean_color_hex(color_hex)

    try:
        return tags_queries.edit_tag(
            user_id,
            tag_id,
            clean_name,
            clean_color,
        )
    except (psycopg.errors.UniqueViolation, psycopg.errors.CheckViolation) as error:
        _raise_friendly_constraint_error(error)


def remove_user_tag(user_id, tag_id):
    _validate_user_id(user_id)
    _validate_tag_id(tag_id)
    tags_queries.delete_tag(user_id, tag_id)


def get_task_tags(user_id, task_id):
    _validate_user_id(user_id)
    if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id <= 0:
        raise ValueError("A valid task_id is required.")

    return tags_queries.get_tags_for_task(user_id, task_id)


def set_tags_for_task(user_id, task_id, tag_ids):
    _validate_user_id(user_id)
    if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id <= 0:
        raise ValueError("A valid task_id is required.")

    clean_tag_ids = _clean_tag_ids(tag_ids)
    tags_queries.replace_task_tags(user_id, task_id, clean_tag_ids)
    return tags_queries.get_tags_for_task(user_id, task_id)


def search_tasks_by_tags(user_id, tag_ids, match_all=False):
    _validate_user_id(user_id)
    clean_tag_ids = _clean_tag_ids(tag_ids)

    if not clean_tag_ids:
        return []

    return task_queries.get_tasks_by_tag_ids(
        user_id,
        clean_tag_ids,
        match_all=bool(match_all),
    )


def create_default_tags_for_user(user_id):
    _validate_user_id(user_id)
    return tags_queries.add_tags(user_id, DEFAULT_TAGS)
