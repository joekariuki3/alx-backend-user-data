#!/usr/bin/env python3
"""Auth module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """ hashes string password
    Returns hashed byte string
    """
    password = password.encode()
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash_password
