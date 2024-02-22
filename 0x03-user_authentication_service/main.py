#!/usr/bin/env python3
"""
end to end Integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test if user is registered and response code
    if not registered also test the response code
    and response message
    """
    data = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/users', data=data)
    if res.status_code == 200:
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "user created"}
    else:
        assert res.status_code == 400
        assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong credectials
    """
    data = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/sessions', data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test login with correct credectials
    """
    data = {"email": email, "password": password}
    res = requests.post('http://localhost:5000/sessions', data=data)
    if res.status_code == 200:
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "logged in"}
        return res.cookies.get('session_id')
    else:
        assert res.status_code == 401


def profile_unlogged() -> None:
    """Test to check for profile of a user when not logged in
    """
    res = requests.get('http://localhost:5000/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test to check for profile of a user when logged in
    """
    cookie_data = {"session_id": session_id}
    res = requests.get('http://localhost:5000/profile', cookies=cookie_data)
    if res.status_code == 200:
        assert res.status_code == 200
        assert res.json() == {"email": EMAIL}
    else:
        assert res.status_code == 403


def log_out(session_id: str) -> None:
    """Test loging out a user who is logged in
    """
    cookie_data = {"session_id": session_id}
    res = requests.delete('http://localhost:5000/sessions',
                          cookies=cookie_data)
    if res.status_code == 403:
        assert res.status_code == 403
    else:
        # 302 redirection was a sucess returns 200 secess
        assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """Test generate a password reset token
    """
    data = {"email": email}
    res = requests.post("http://localhost:5000/reset_password", data=data)
    if res.status_code == 200:
        token = res.json().get("reset_token")
        assert res.status_code == 200
        assert res.json() == {"email": email, "reset_token": token}
        return token
    else:
        assert res.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test change user password to a new one
    """
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    res = requests.put('http://localhost:5000/reset_password', data=data)
    if res.status_code == 200:
        assert res.status_code == 200
        assert res.json() == {"email": email, "message": "Password updated"}
    else:
        assert res.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
