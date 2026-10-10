
from flask import Blueprint
from controllers.student_controller import (
    add_student,
    get_students,
    get_student,
    update_student,
    delete_student
)
from middlewares.auth_middleware import token_required, role_required

student_routes = Blueprint("student_routes", __name__)

# USER and ADMIN - View students
student_routes.route("/students", methods=["GET"])(
    token_required(get_students)
)

student_routes.route("/students/<int:id>", methods=["GET"])(
    token_required(get_student)
)

# ADMIN only - Add student
student_routes.route("/students", methods=["POST"])(
    token_required(role_required("ADMIN")(add_student))
)

# ADMIN only - Update student
student_routes.route("/students/<int:id>", methods=["PUT"])(
    token_required(role_required("ADMIN")(update_student))
)

# ADMIN only - Delete student
student_routes.route("/students/<int:id>", methods=["DELETE"])(
    token_required(role_required("ADMIN")(delete_student))
)