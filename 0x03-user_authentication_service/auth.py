#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """ hashes string password
    Returns hashed byte string
    """
    password = password.encode()
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash_password


def _generate_uuid() -> str:
    """Return a uniq string id
    """
    new_id = str(uuid.uuid4())
    return new_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ creates a user with email as email and password as password
        Returns user object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hash_pwd = _hash_password(password)
            user = self._db.add_user(email, hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Return True if password matches else False
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(),  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session or user with email passed
        Returns sessionID
        """
        try:
            user = self._db.find_user_by(email=email)
            user_session_id = _generate_uuid()
            setattr(user, "session_id", user_session_id)
            return user_session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns a user assosciated with a session ID
        else None
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys user session
        """
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            setattr(user, "session_id", None)
            return None
        except NoResultFound:
            return None
