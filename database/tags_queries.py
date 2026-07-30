from database.db import get_db_connection


def _tag_from_row(row):
    return {
        "tag_id": row[0],
        "tag_name": row[1],
        "color_hex": row[2],
        "date_created": row[3],
    }


def add_tag(user_id, tag_name, color_hex):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tags (user_id, tag_name, color_hex)
                VALUES (%s, %s, %s)
                RETURNING tag_id, tag_name, color_hex, date_created;
                """,
                (user_id, tag_name, color_hex),
            )
            row = cur.fetchone()

            if row is None:
                raise ValueError("Tag insert failed. No tag returned.")

            return _tag_from_row(row)


def add_tags(user_id, tags):
    created_tags = []

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for tag_name, color_hex in tags:
                cur.execute(
                    """
                    INSERT INTO tags (user_id, tag_name, color_hex)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING
                    RETURNING tag_id, tag_name, color_hex, date_created;
                    """,
                    (user_id, tag_name, color_hex),
                )
                row = cur.fetchone()
                if row is not None:
                    created_tags.append(_tag_from_row(row))

    return created_tags


def get_tags(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tag_id, tag_name, color_hex, date_created
                FROM tags
                WHERE user_id = %s
                ORDER BY lower(tag_name), tag_id;
                """,
                (user_id,),
            )
            return [_tag_from_row(row) for row in cur.fetchall()]


def get_tag(user_id, tag_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tag_id, tag_name, color_hex, date_created
                FROM tags
                WHERE user_id = %s
                    AND tag_id = %s;
                """,
                (user_id, tag_id),
            )
            row = cur.fetchone()
            return _tag_from_row(row) if row is not None else None


def get_tag_id_by_name(user_id, tag_name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tag_id
                FROM tags
                WHERE user_id = %s
                    AND lower(tag_name) = lower(%s);
                """,
                (user_id, tag_name),
            )
            row = cur.fetchone()
            return row[0] if row is not None else None


def edit_tag(user_id, tag_id, new_tag_name, new_color_hex):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tags
                SET tag_name = %s,
                    color_hex = %s
                WHERE user_id = %s
                    AND tag_id = %s
                RETURNING tag_id, tag_name, color_hex, date_created;
                """,
                (new_tag_name, new_color_hex, user_id, tag_id),
            )
            row = cur.fetchone()

            if row is None:
                raise ValueError("Tag update failed. No matching tag found.")

            return _tag_from_row(row)


def delete_tag(user_id, tag_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tags
                WHERE user_id = %s
                    AND tag_id = %s;
                """,
                (user_id, tag_id),
            )

            if cur.rowcount == 0:
                raise ValueError("Tag delete failed. No matching tag found.")


def get_tags_for_task(user_id, task_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tags.tag_id,
                    tags.tag_name,
                    tags.color_hex,
                    tags.date_created
                FROM task_tags
                INNER JOIN tags
                    ON task_tags.user_id = tags.user_id
                    AND task_tags.tag_id = tags.tag_id
                WHERE task_tags.user_id = %s
                    AND task_tags.task_id = %s
                ORDER BY lower(tags.tag_name), tags.tag_id;
                """,
                (user_id, task_id),
            )
            return [_tag_from_row(row) for row in cur.fetchall()]


def replace_task_tags(user_id, task_id, tag_ids):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM tasks
                WHERE user_id = %s
                    AND task_id = %s;
                """,
                (user_id, task_id),
            )
            if cur.fetchone() is None:
                raise ValueError("Task tag update failed. No matching task found.")

            if tag_ids:
                cur.execute(
                    """
                    SELECT tag_id
                    FROM tags
                    WHERE user_id = %s
                        AND tag_id = ANY(%s);
                    """,
                    (user_id, tag_ids),
                )
                found_tag_ids = {row[0] for row in cur.fetchall()}
                missing_tag_ids = set(tag_ids) - found_tag_ids
                if missing_tag_ids:
                    raise ValueError(
                        "Task tag update failed. One or more tags do not belong to the user."
                    )

            cur.execute(
                """
                DELETE FROM task_tags
                WHERE user_id = %s
                    AND task_id = %s;
                """,
                (user_id, task_id),
            )

            cur.executemany(
                """
                INSERT INTO task_tags (user_id, task_id, tag_id)
                VALUES (%s, %s, %s);
                """,
                [(user_id, task_id, tag_id) for tag_id in tag_ids],
            )
