from database.db import get_db_connection

def add_user(username, hpassword):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO users (
                        username,
                        hpassword) 
                        VALUES (?, ?)
                        RETURN user_id;
                        """,
                        (username, hpassword)
                        )

    conn.commit()
    conn.close()

def get_user():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT 
                username,
                hpassword AS bytes.fromhex(hpassword)
            FROM users;
            """)
