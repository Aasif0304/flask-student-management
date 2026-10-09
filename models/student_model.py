from config import get_db_connection


def create_student(data):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students (name, age, course)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (data["name"], data["age"], data["course"])
    )

    student_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return student_id


def fetch_all_students():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.age,
            s.course,
            f.total_fees,
            f.paid_fees,
            f.pending_fees
        FROM students s
        LEFT JOIN fees f ON s.id = f.student_id
        ORDER BY s.id
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3],
            "total_fees": float(row[4]) if row[4] is not None else 0,
            "paid_fees": float(row[5]) if row[5] is not None else 0,
            "pending_fees": float(row[6]) if row[6] is not None else 0
        }
        for row in rows
    ]
def fetch_student_by_id(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            s.id,
            s.name,
            s.age,
            s.course,
            f.total_fees,
            f.paid_fees,
            f.pending_fees
        FROM students s
        LEFT JOIN fees f ON s.id = f.student_id
        WHERE s.id = %s
        """,
        (student_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "age": row[2],
        "course": row[3],
        "total_fees": float(row[4]) if row[4] is not None else 0,
        "paid_fees": float(row[5]) if row[5] is not None else 0,
        "pending_fees": float(row[6]) if row[6] is not None else 0
    }

def edit_student(student_id, data):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name = %s, age = %s, course = %s
        WHERE id = %s
        """,
        (data["name"], data["age"], data["course"], student_id)
    )

    updated = cursor.rowcount > 0
    connection.commit()
    cursor.close()
    connection.close()

    return updated


def remove_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    deleted = cursor.rowcount > 0
    connection.commit()
    cursor.close()
    connection.close()

    return deleted