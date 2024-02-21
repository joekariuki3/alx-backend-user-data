#!/usr/bin/env python3
"""Flask app"""
from auth import Auth
from flask import (Flask, jsonify,
                   request, abort,
                   make_response,
                   redirect, url_for)

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
    session_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """Destroys the session
    """
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.find_user_by(session_id=session_id)
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    except NoResultFound:
        abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
