#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home() -> str:
    """home route/ default route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """creates a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        message = {"email": email, "message": "user created"}
        return jsonify(message)
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Creates a new session for user if email and password match
    that are in the request
    Returns a success message or aborts with 401
    """
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid = AUTH.valid_login(email, password)
    if not is_valid:
        abort(401)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
