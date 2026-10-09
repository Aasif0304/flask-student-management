
from flask import Blueprint
from controllers.fees_controller import create_student_fees, get_student_fees, update_student_fees, delete_student_fees

fees_routes = Blueprint("fees_routes", __name__)

fees_routes.route("/fees", methods=["POST"])(create_student_fees)
fees_routes.route("/fees/<int:student_id>", methods=["GET"])(get_student_fees)
fees_routes.route("/fees/<int:student_id>", methods=["PUT"])(update_student_fees)
fees_routes.route("/fees/<int:student_id>", methods=["DELETE"])(delete_student_fees)