from config import get_db_connection


def create_users_table():
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'USER'
                    CHECK (role IN ('ADMIN', 'USER'))
            )
        """)

        conn.commit()
        print("Users table created successfully")

    except Exception as e:
        conn.rollback()
        print("Error creating users table:", e)

    finally:
        if cursor:
            cursor.close()
        conn.close()


def register_user(name, email, password):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, role
            """,
            (name, email, password)
        )

        user = cursor.fetchone()
        conn.commit()

        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3]
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        conn.close()
        
def get_user_by_email(email):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()
        conn.close()