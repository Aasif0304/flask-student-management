from flask import Blueprint
from controllers.student_controller import (
    add_student,
    get_students,
    get_student,
    update_student,
    delete_student
)

student_routes = Blueprint("student_routes", __name__)

student_routes.route("/students", methods=["POST"])(add_student)
student_routes.route("/students", methods=["GET"])(get_students)
student_routes.route("/students/<int:id>", methods=["GET"])(get_student)
student_routes.route("/students/<int:id>", methods=["PUT"])(update_student)
student_routes.route("/students/<int:id>", methods=["DELETE"])(delete_student)