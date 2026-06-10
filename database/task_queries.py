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
                    due_date,
                    difficulty,
                    estimated_hours
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURN task_id;
                """,
                (user_id, task['task'], task['course'], task['due_date'], task['difficulty'], task['hours'])
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
                    due_date,
                    difficulty,
                    estimated_hours
                FROM tasks 
                WHERE user_id = %s;
                """,
                (user_id, )
            )
            rows = cur.fetchall()
            return rows
