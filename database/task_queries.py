from database.db import get_db_connection

def add_task(user_id, task):
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
                    date_completed
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                )
            )
            row = cur.fetchone()

            if row is None:
                raise ValueError("Task insert failed. No task_id returned.")

            return row[0]

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
                    tasks.date_completed
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
                })

            return tasks
        
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
