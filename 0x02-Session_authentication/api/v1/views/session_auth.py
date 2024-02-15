#!/usr/bin/env python3

"""Module for session views
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def log_in():
    """ceates a session if a user is authenticated
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email:
        error_data = {"error": "email missing"}
        return jsonify(error_data), 400
    if not password:
        error_data = {"error": "password missing"}
        return jsonify(error_data), 400
    # retrieve user based on the email
    user = None
    try:
        result = User.search({"email": email})
        if len(result) > 0:
            user = result[0]
    except KeyError:
        error_data = {"error": "no user found for this email"}
        return jsonify(error_data), 404
    if not user:
        error_data = {"error": "no user found for this email"}
        return jsonify(error_data), 404
    # check if password is valid
    if not user.is_valid_password(password):
        error_data = {"error": "wrong password"}
        return jsonify(error_data), 401
    # creat a sessionID for the user ID
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    # set the cookie to the response
    session_name = getenv("SESSION_NAME")
    response = make_response(user.to_json())
    response.set_cookie(session_name, session_id)
    return response
