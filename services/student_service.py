from models.student_model import (
    create_student,
    fetch_all_students,
    fetch_student_by_id,
    edit_student,
    remove_student
)


def add_student(data):
    return create_student(data)


def get_students():
    return fetch_all_students()


def get_student(student_id):
    return fetch_student_by_id(student_id)


def update_student(student_id, data):
    return edit_student(student_id, data)


def delete_student(student_id):
    return remove_student(student_id)