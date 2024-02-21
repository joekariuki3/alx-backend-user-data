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

    @property
    def _generate_uuid(self) -> str:
        """Return a uniq string id"""
        new_id = uuid.uuid4()
        return new_id
