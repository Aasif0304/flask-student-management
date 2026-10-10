from flask import request, jsonify
from services.auth_service import register_service, login_service


def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON body is required"}), 400

    response, status_code = register_service(data)

    return jsonify(response), status_code


def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON body is required"}), 400

    response, status_code = login_service(data)

    return jsonify(response), status_code