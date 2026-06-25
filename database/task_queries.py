from database.db import get_db_connection

def add_task(user_id, task):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tasks (
                    user_id,
                    task_name,
                    course_name,
                    estimated_hours,
                    hours_used,
                    completion_status,
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
                    task["course"],
                    task["hours"] if not task["completed"] else None,
                    task["hours"] if task["completed"] else None,
                    task["completed"],
                    task["difficulty"],
                    task["due_date"],
                    task["date_completed"],
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
                    task_id,
                    task_name,
                    course_name,
                    completion_status,
                    difficulty_level,
                    estimated_hours,
                    hours_used,
                    due_date,
                    date_completed
                FROM tasks 
                WHERE user_id = %s;
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            tasks = []
            for row in rows:
                tasks.append({
                    "task_id": row[0],
                    "task": row[1],
                    "course": row[2],
                    "completed": row[3],
                    "difficulty": row[4],
                    "hours": row[5] if row[5] is not None else row[6],
                    "due_date": row[7],
                    "date_completed": row[8],
                })

            return tasks
        
def update_task(task_id, updated_task):
    if updated_task["completed"]:
        estimated_hours = None
        hours_used = updated_task["hours"]
        due_date = None
        date_completed = updated_task["date_completed"]
    else:
        estimated_hours = updated_task["hours"]
        hours_used = None
        due_date = updated_task["due_date"]
        date_completed = None

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET task_name = %s,
                    course_name = %s,
                    estimated_hours = %s,
                    hours_used = %s,
                    completion_status = %s,
                    difficulty_level = %s,
                    due_date = %s,
                    date_completed = %s
                WHERE task_id = %s;
                """,
                (
                    updated_task["task"],
                    updated_task["course"],
                    estimated_hours,
                    hours_used,
                    updated_task["completed"],
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