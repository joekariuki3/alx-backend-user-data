#!/usr/bin/env python3
"""returns an encripted password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """return a salted, harshed pasword that is byte string"""
    encoded_password = password.encode()
    hash_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hash_password
