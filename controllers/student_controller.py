from flask import request, jsonify
from services.student_service import (
    add_student as create_student,
    get_students as fetch_students,
    get_student as fetch_student,
    update_student as edit_student,
    delete_student as remove_student
)


def add_student():
    data = request.get_json()
    student_id = create_student(data)

    return jsonify({
        "message": "Student added successfully",
        "id": student_id
    }), 201


def get_students():
    return jsonify(fetch_students())


def get_student(id):
    student = fetch_student(id)

    if student is None:
        return jsonify({"message": "Student not found"}), 404

    return jsonify(student)


def update_student(id):
    data = request.get_json()

    if not edit_student(id, data):
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})


def delete_student(id):
    if not remove_student(id):
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})