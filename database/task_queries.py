from database.db import get_db_connection


def add_task(user_id, task, tags=None):
    tags = tags or []

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (
                    user_id,
                    task_name,
                    course_id,
                    estimated_hours,
                    hours_used,
                    status,
                    difficulty_level,
                    due_date,
                    date_completed,
                    short_description
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING task_id;
                """,
                (
                    user_id,
                    task["task"],
                    task["course_id"],
                    task.get("estimated_hours"),
                    task.get("hours_used"),
                    task["status"],
                    task["difficulty"],
                    task.get("due_date"),
                    task.get("date_completed"),
                    task.get("short_description"),
                )
            )
            row = cur.fetchone()

            if row is None:
                raise ValueError("Task insert failed. No task_id returned.")

            task_id = row[0]
            tag_ids = []

            for tag in tags:
                tag_id = tag.get("tag_id")

                if tag_id is None:
                    cur.execute(
                        """
                        INSERT INTO tags (user_id, tag_name, color_hex)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (user_id, (lower(tag_name)))
                        DO UPDATE SET color_hex = EXCLUDED.color_hex
                        RETURNING tag_id;
                        """,
                        (
                            user_id,
                            tag["tag_name"].strip(),
                            tag["color_hex"],
                        ),
                    )
                    tag_row = cur.fetchone()
                    if tag_row is None:
                        raise ValueError("Tag insert failed. No tag_id returned.")
                    tag_id = tag_row[0]

                if tag_id not in tag_ids:
                    tag_ids.append(tag_id)

            cur.executemany(
                """
                INSERT INTO task_tags (user_id, task_id, tag_id)
                VALUES (%s, %s, %s);
                """,
                [(user_id, task_id, tag_id) for tag_id in tag_ids],
            )

            return task_id


def get_tasks(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tasks.task_id,
                    tasks.task_name,
                    courses.course_id,
                    courses.course_name,
                    tasks.status,
                    tasks.difficulty_level,
                    tasks.estimated_hours,
                    tasks.hours_used,
                    tasks.due_date,
                    tasks.date_completed,
                    tasks.short_description
                FROM tasks
                INNER JOIN courses
                    ON tasks.user_id = courses.user_id
                    AND tasks.course_id = courses.course_id
                WHERE tasks.user_id = %s;
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            tasks = []
            for row in rows:
                tasks.append({
                    "task_id": row[0],
                    "task": row[1],
                    "course_id": row[2],
                    "course": row[3],
                    "status": row[4],
                    "difficulty": row[5],
                    "estimated_hours": row[6],
                    "hours_used": row[7],
                    "due_date": row[8],
                    "date_completed": row[9],
                    "short_description": row[10],
                })

            return tasks


def get_tasks_by_course(course_name, user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    tasks.task_id,
                    tasks.task_name,
                    courses.course_id,
                    courses.course_name,
                    tasks.status,
                    tasks.difficulty_level,
                    tasks.estimated_hours,
                    tasks.hours_used,
                    tasks.due_date,
                    tasks.date_completed,
                    tasks.short_description
                FROM tasks
                INNER JOIN courses
                    ON tasks.user_id = courses.user_id
                    AND tasks.course_id = courses.course_id
                WHERE courses.course_name = %s AND tasks.user_id = %s;
                """,
                (course_name, user_id)
            )

            rows = cur.fetchall()

            tasks = []
            for row in rows:
                tasks.append({
                    "task_id": row[0],
                    "task": row[1],
                    "course_id": row[2],
                    "course": row[3],
                    "status": row[4],
                    "difficulty": row[5],
                    "estimated_hours": row[6],
                    "hours_used": row[7],
                    "due_date": row[8],
                    "date_completed": row[9],
                    "short_description": row[10],
                })

            return tasks


def get_tasks_by_tag_ids(user_id, tag_ids, match_all=False):
    comparison = "= %s" if match_all else ">= 1"
    parameters = [user_id, tag_ids]
    if match_all:
        parameters.append(len(tag_ids))

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    tasks.task_id,
                    tasks.task_name,
                    courses.course_id,
                    courses.course_name,
                    tasks.status,
                    tasks.difficulty_level,
                    tasks.estimated_hours,
                    tasks.hours_used,
                    tasks.due_date,
                    tasks.date_completed,
                    tasks.short_description
                FROM tasks
                INNER JOIN courses
                    ON tasks.user_id = courses.user_id
                    AND tasks.course_id = courses.course_id
                INNER JOIN task_tags
                    ON tasks.user_id = task_tags.user_id
                    AND tasks.task_id = task_tags.task_id
                WHERE tasks.user_id = %s
                    AND task_tags.tag_id = ANY(%s)
                GROUP BY
                    tasks.task_id,
                    courses.course_id,
                    courses.course_name
                HAVING COUNT(DISTINCT task_tags.tag_id) {comparison}
                ORDER BY tasks.due_date NULLS LAST, tasks.task_id;
                """,
                parameters,
            )

            return [
                {
                    "task_id": row[0],
                    "task": row[1],
                    "course_id": row[2],
                    "course": row[3],
                    "status": row[4],
                    "difficulty": row[5],
                    "estimated_hours": row[6],
                    "hours_used": row[7],
                    "due_date": row[8],
                    "date_completed": row[9],
                    "short_description": row[10],
                }
                for row in cur.fetchall()
            ]


def update_task(task_id, updated_task):
    status = updated_task["status"]
    estimated_hours = updated_task.get("estimated_hours")
    hours_used = updated_task.get("hours_used")
    due_date = updated_task.get("due_date")
    date_completed = updated_task.get("date_completed")

    if status == "not_started":
        hours_used = None
        date_completed = None
    elif status == "in_progress":
        date_completed = None
    elif status == "completed":
        due_date = None

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET task_name = %s,
                    course_id = %s,
                    estimated_hours = %s,
                    hours_used = %s,
                    status = %s,
                    difficulty_level = %s,
                    due_date = %s,
                    date_completed = %s
                WHERE task_id = %s;
                """,
                (
                    updated_task["task"],
                    updated_task["course_id"],
                    estimated_hours,
                    hours_used,
                    status,
                    updated_task["difficulty"],
                    due_date,
                    date_completed,
                    task_id,
                )
            )

            if cur.rowcount == 0:
                raise ValueError("Task update failed. No rows affected.")

def delete_task(task_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM tasks
                WHERE task_id = %s;
                """,
                (task_id, )
            )
            if cur.rowcount == 0:
                raise ValueError("Task delete failed. No rows affected.")
