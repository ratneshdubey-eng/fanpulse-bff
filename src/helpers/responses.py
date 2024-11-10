from flask import jsonify, make_response

def error_response(message: str, status_code: int):
    response = jsonify({"error": message})
    response.status_code = status_code
    return response

def success_response(data, status_code: int = 200):
    return make_response(jsonify(data), status_code)
