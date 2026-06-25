from database.db import get_db_connection

def create_user(username, email, password_hash):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (
                username,
                email,
                password_hash
                )
                VALUES (%s, %s, %s)
                RETURNING user_id, username, email;
                """,
                (username, email, password_hash)
            )
            user = cur.fetchone()

            if user is None:
                raise ValueError("User was not created.")
            return {
                "user_id": user[0],
                "username": user[1],
                "email": user[2]
            }

def get_user_by_username(username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    user_id,
                    username,
                    email,
                    password_hash
                FROM users
                WHERE username = %s;
                """, 
                (username,)
                )
            
            user = cur.fetchone()

            if user is None:
                return None
            
            return {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "password_hash": user[3]
            }

def get_user_by_id(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT 
                user_id,
                username,
                email,
                password_hash
            FROM users
            WHERE user_id = %s;
            """, 
            (user_id,)
            )

            user = cur.fetchone()

            if user is None:
                return None
            return {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "password_hash": user[3]
            }
        
def update_username(user_id, new_username):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE users
            SET username = %s
            WHERE user_id = %s;
            """, 
            (new_username, user_id)
            )

def update_email(user_id, new_email):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE users
            SET email = %s
            WHERE user_id = %s;
            """, 
            (new_email, user_id)
            )

def update_password(user_id, new_password_hash):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            UPDATE users
            SET password_hash = %s
            WHERE user_id = %s;
            """, 
            (new_password_hash, user_id)
            )

def delete_user(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DELETE FROM users
            WHERE user_id = %s;
            """, 
            (user_id,)
            )