#!/usr/bin/env python3
"""returns an encripted password"""

from bcrypt import hashpw, gensalt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """takes a  string password, hashes it and return a byte string"""
    encoded_password = password.encode("utf-8")
    hash_password = hashpw(encoded_password, gensalt())
    return hash_password
