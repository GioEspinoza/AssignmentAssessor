from database.db import get_db_connection


def add_course(user_id, course_name, course_code=None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO courses (
                    user_id,
                    course_name,
                    course_code
                )
                VALUES (%s, %s, %s)
                RETURNING course_id;
                """,
                (user_id, course_name, course_code)
            )
            row = cur.fetchone()

            if row is None:
                raise ValueError("Course insert failed. No course_id returned.")

            return row[0]


def get_active_courses(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    course_id,
                    course_name,
                    course_code,
                    is_active,
                    date_created
                FROM courses
                WHERE user_id = %s
                    AND is_active = true
                ORDER BY course_name;
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            courses = []
            for row in rows:
                courses.append({
                    "course_id": row[0],
                    "course_name": row[1],
                    "course_code": row[2],
                    "is_active": row[3],
                    "date_created": row[4],
                })

            return courses


def get_courses(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    course_id,
                    course_name,
                    course_code,
                    is_active,
                    date_created
                FROM courses
                WHERE user_id = %s
                ORDER BY is_active DESC, course_name;
                """,
                (user_id,)
            )

            rows = cur.fetchall()

            courses = []
            for row in rows:
                courses.append({
                    "course_id": row[0],
                    "course_name": row[1],
                    "course_code": row[2],
                    "is_active": row[3],
                    "date_created": row[4],
                })

            return courses


def archive_course(user_id, course_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE courses
                SET is_active = false
                WHERE user_id = %s
                    AND course_id = %s;
                """,
                (user_id, course_id)
            )

            if cur.rowcount == 0:
                raise ValueError("Course archive failed. No rows affected.")


def restore_course(user_id, course_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE courses
                SET is_active = true
                WHERE user_id = %s
                    AND course_id = %s;
                """,
                (user_id, course_id)
            )

            if cur.rowcount == 0:
                raise ValueError("Course restore failed. No rows affected.")
