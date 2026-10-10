
from flask import Blueprint
from controllers.fees_controller import (
    create_student_fees,
    get_student_fees,
    update_student_fees,
    delete_student_fees
)
from middlewares.auth_middleware import token_required, role_required

fees_routes = Blueprint("fees_routes", __name__)

# ADMIN only - Add fees
fees_routes.route("/fees", methods=["POST"])(
    token_required(role_required("ADMIN")(create_student_fees))
)

# USER and ADMIN - View fees
fees_routes.route("/fees/<int:student_id>", methods=["GET"])(
    token_required(get_student_fees)
)

# ADMIN only - Update fees
fees_routes.route("/fees/<int:student_id>", methods=["PUT"])(
    token_required(role_required("ADMIN")(update_student_fees))
)

# ADMIN only - Delete fees
fees_routes.route("/fees/<int:student_id>", methods=["DELETE"])(
    token_required(role_required("ADMIN")(delete_student_fees))
)