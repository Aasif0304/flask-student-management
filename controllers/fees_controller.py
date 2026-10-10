
from flask import request, jsonify
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from services.fees_service import add_fees, get_fees_by_student_id, edit_fees, remove_fees

def create_student_fees():
    data = request.get_json(silent=True)
    required_fields = ["student_id", "total_fees", "paid_fees"]
    if not isinstance(data, dict) or any(field not in data for field in required_fields):
        return jsonify({"error": "student_id, total_fees, paid_fees are required"}), 400
    try:
        student_id = int(data["student_id"])
        total_fees = float(data["total_fees"])
        paid_fees = float(data["paid_fees"])
        if student_id <= 0:
            return jsonify({"error": "student_id must be a positive integer"}), 400
        if total_fees < 0 or paid_fees < 0:
            return jsonify({"error": "Fees cannot be negative"}), 400
        if paid_fees > total_fees:
            return jsonify({"error": "Paid fees cannot exceed total fees"}), 400
        data["student_id"] = student_id
        data["total_fees"] = total_fees
        data["paid_fees"] = paid_fees
        fees_id = add_fees(data)
        return jsonify({"message": "Fees added successfully", "id": fees_id}), 201
    except ForeignKeyViolation:
        return jsonify({"error": "Student not found. Please provide a valid student_id"}), 404
    except UniqueViolation as error:
        if error.diag.constraint_name == "fees_student_id_key":
            return jsonify({"error": "Fees record already exists for this student"}), 409
        return jsonify({"error": "Duplicate record conflict"}), 409
    except (TypeError, ValueError):
        return jsonify({"error": "Student ID and fees values must be valid numbers"}), 400

def get_student_fees(student_id):
    fees = get_fees_by_student_id(student_id)
    if fees is None:
        return jsonify({"message": "Fees not found for this student"}), 404
    return jsonify(fees), 200

def update_student_fees(student_id):
    data = request.get_json(silent=True)
    required_fields = ["total_fees", "paid_fees"]
    if not isinstance(data, dict) or any(field not in data for field in required_fields):
        return jsonify({"error": "total_fees and paid_fees are required"}), 400
    try:
        total_fees = float(data["total_fees"])
        paid_fees = float(data["paid_fees"])
        if total_fees < 0 or paid_fees < 0:
            return jsonify({"error": "Fees cannot be negative"}), 400
        if paid_fees > total_fees:
            return jsonify({"error": "Paid fees cannot exceed total fees"}), 400
        fees_id = edit_fees(student_id, {"total_fees": total_fees, "paid_fees": paid_fees})
        if fees_id is None:
            return jsonify({"message": "Fees not found for this student"}), 404
        return jsonify({"message": "Fees updated successfully", "id": fees_id}), 200
    except (TypeError, ValueError):
        return jsonify({"error": "Fees values must be valid numbers"}), 400

def delete_student_fees(student_id):
    fees_id = remove_fees(student_id)
    if fees_id is None:
        return jsonify({"message": "Fees not found for this student"}), 404
    return jsonify({"message": "Fees deleted successfully", "id": fees_id}), 200