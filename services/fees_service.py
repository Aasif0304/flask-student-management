
from models.fees_model import create_fees, fetch_fees_by_student_id, update_fees, delete_fees

def add_fees(data):
    return create_fees(data)

def get_fees_by_student_id(student_id):
    return fetch_fees_by_student_id(student_id)

def edit_fees(student_id, data):
    return update_fees(student_id, data)

def remove_fees(student_id):
    return delete_fees(student_id)