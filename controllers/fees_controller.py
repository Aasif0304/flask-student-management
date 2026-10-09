
from flask import request, jsonify
from services.fees_service import add_fees, get_fees_by_student_id, edit_fees

def create_student_fees():
    data = request.get_json()
    required_fields = ["student_id", "total_fees", "paid_fees"]
    if not data or any(field not in data for field in required_fields):
        return jsonify({"message": "student_id, total_fees, paid_fees are required"}), 400
    try:
        total_fees = float(data["total_fees"])
        paid_fees = float(data["paid_fees"])
        if total_fees < 0 or paid_fees < 0:
            return jsonify({"message": "Fees cannot be negative"}), 400
        if paid_fees > total_fees:
            return jsonify({"message": "Paid fees cannot exceed total fees"}), 400
        data["total_fees"] = total_fees
        data["paid_fees"] = paid_fees
        fees_id = add_fees(data)
        return jsonify({"message": "Fees added successfully", "id": fees_id}), 201
    except (TypeError, ValueError):
        return jsonify({"message": "Fees values must be valid numbers"}), 400

def get_student_fees(student_id):
    fees = get_fees_by_student_id(student_id)
    if fees is None:
        return jsonify({"message": "Fees not found for this student"}), 404
    return jsonify(fees), 200

def update_student_fees(student_id):
    data = request.get_json()
    required_fields = ["total_fees", "paid_fees"]
    if not data or any(field not in data for field in required_fields):
        return jsonify({"message": "total_fees and paid_fees are required"}), 400
    try:
        total_fees = float(data["total_fees"])
        paid_fees = float(data["paid_fees"])
        if total_fees < 0 or paid_fees < 0:
            return jsonify({"message": "Fees cannot be negative"}), 400
        if paid_fees > total_fees:
            return jsonify({"message": "Paid fees cannot exceed total fees"}), 400
        fees_id = edit_fees(student_id, {"total_fees": total_fees, "paid_fees": paid_fees})
        if fees_id is None:
            return jsonify({"message": "Fees not found for this student"}), 404
        return jsonify({"message": "Fees updated successfully", "id": fees_id}), 200
    except (TypeError, ValueError):
        return jsonify({"message": "Fees values must be valid numbers"}), 400
    

def delete_student_fees(student_id):
    from services.fees_service import remove_fees

    fees_id = remove_fees(student_id)
    if fees_id is None:
        return jsonify({"message": "Fees not found for this student"}), 404
    return jsonify({"message": "Fees deleted successfully", "id": fees_id}), 200