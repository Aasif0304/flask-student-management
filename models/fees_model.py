from config import get_db_connection

def create_fees(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO fees (student_id, total_fees, paid_fees, pending_fees)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (data["student_id"], data["total_fees"], data["paid_fees"], data["total_fees"] - data["paid_fees"]))
        fees_id = cursor.fetchone()[0]
        connection.commit()
        return fees_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

def fetch_fees_by_student_id(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT id, student_id, total_fees, paid_fees, pending_fees
            FROM fees WHERE student_id = %s
        """, (student_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return {
            "id": row[0],
            "student_id": row[1],
            "total_fees": float(row[2]),
            "paid_fees": float(row[3]),
            "pending_fees": float(row[4])
        }
    finally:
        cursor.close()
        connection.close()

def update_fees(student_id, data):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE fees
            SET total_fees = %s, paid_fees = %s, pending_fees = %s
            WHERE student_id = %s
            RETURNING id
        """, (data["total_fees"], data["paid_fees"], data["total_fees"] - data["paid_fees"], student_id))
        row = cursor.fetchone()
        if row is None:
            connection.rollback()
            return None
        connection.commit()
        return row[0]
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
        

def delete_fees(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM fees WHERE student_id = %s RETURNING id",
            (student_id,)
        )
        row = cursor.fetchone()
        if row is None:
            connection.rollback()
            return None
        connection.commit()
        return row[0]
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()