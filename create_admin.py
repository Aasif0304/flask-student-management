
from config import get_db_connection


def promote_user_to_admin():
    email = input("Enter registered user's email: ").strip().lower()

    if not email:
        print("Email is required.")
        return

    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET role = 'ADMIN'
            WHERE LOWER(email) = %s
            RETURNING id, name, email, role
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user is None:
            conn.rollback()
            print("User not found. Register the user first.")
            return

        conn.commit()

        print("\nUser promoted to ADMIN successfully!")
        print(f"ID: {user[0]}")
        print(f"Name: {user[1]}")
        print(f"Email: {user[2]}")
        print(f"Role: {user[3]}")

    except Exception as error:
        conn.rollback()
        print("Admin setup failed:", error)

    finally:
        if cursor:
            cursor.close()
        conn.close()


if __name__ == "__main__":
    promote_user_to_admin()   